from .github import Github
from .group import Group
from .google import Google
from .user import User
from loguru import logger
from shared.clientapi import ClientApi as Client
from shared import Env, parallel, SyncAction, Const
from .members import Members
from .db import DB

class SyncData:
    def __init__(self):
        self.gws_groups: [Group] = []
        self.gws_users: [User] = []
        self.gh_groups: [Group] = []
        self.email_gh_usernames: [dict] = []
        self.root_gh_team_id = ""
        self.root_custom_gh_team_id = ""
        self.gh_pending_invites = []
        self.gh_legacy_inactive_users = []

class Sync():
    def __init__(self, client: Client):
        self.__sync_data = SyncData()
        self.__client = client
        self.__github_groups = Github()
        self.__db = DB(filename="hodor.db")

    def sync(self, sync_group: str) -> SyncData:
        """Full sync teams on GitHub from GWS data
        return:
            SyncData can be reused to sync users and avoid fetch the same data on providers
        """
        gws_groups = Members().list_sub_groups(sync_group, email_suffixes_allow=Const.EMAIL_SUFFIX)

        self.__sync_data.gws_groups = Group.from_gws_groups(gws_groups)

        self.__sync_data.root_gh_team_id = self.__github_groups.get(Env.GH_ROOT_TEAM)["id"]
        self.__sync_data.root_custom_gh_team_id = self.__github_groups.get(Env.GH_ROOT_CUSTOM_TEAM)["id"]

        gh_groups = self.__github_groups.list_teams(self.__sync_data.root_gh_team_id)

        gh_groups.extend(self.__github_groups.list_teams(self.__sync_data.root_custom_gh_team_id))

        self.__sync_data.gh_groups = Group.from_gh_teams(gh_groups)

        self.__sync_gws_to_gh()

        self.__sync_gh_to_gws()

        gh_groups = self.__github_groups.list_teams(self.__sync_data.root_gh_team_id)
        gh_groups.extend(self.__github_groups.list_teams(self.__sync_data.root_custom_gh_team_id))
        # mock the created and removed teams on dry run
        if Env.DRY_RUN:
            self.__sync_data.gh_groups = [g for g in self.__sync_data.gh_groups if g.sync_action != SyncAction.REMOVED]
            for g in self.__sync_data.gws_groups:
                gh_group = next((gru for gru in self.__sync_data.gh_groups if gru.name == g.name), None)
                if gh_group is None:
                    self.__sync_data.gh_groups.append(Group(g.email, g.name, ""))
        else:
            self.__sync_data.gh_groups = Group.from_gh_teams(gh_groups)
        # logger.info(f"{self.__client.logkey}update GH sync data end")

        return self.__sync_data

    def __sync_gws_to_gh(self):
        """Sync Google Work Space groups and subgroups into GitHub teams
        """
        result = parallel.execute(
            method=self.__sync_from_google_work_space,
            args_list=[{'group': group} for group in self.__sync_data.gws_groups])
        if result.has_errors():
            raise Exception("sync groups failed")

        count = {
            'created': 0,
            'patched': 0,
            'in-sync': 0
        }

        for group in self.__sync_data.gws_groups:
            if group.sync_action == SyncAction.CREATED:
                count['created'] += 1
            elif group.sync_action == SyncAction.PATCHED:
                count['patched'] += 1
            elif group.sync_action == SyncAction.INSYNC:
                count['in-sync'] += 1

        # logger.info(f"{self.__client.logkey}created={count['created']:,}")
        # logger.info(f"{self.__client.logkey}in-sync={count['in-sync']:,}")
        # logger.info(f"{self.__client.logkey}patched={count['patched']:,}")

    def __sync_from_google_work_space(self, group):
        try:
            gh_group = next((g for g in self.__sync_data.gh_groups if g.name == group.name), None)
            group_in_persistence = self.__db.retrieve(group.id)

            #TODO CHECK WITH DB INFORMATION
            if gh_group is None and group_in_persistence is None:
                gh_group_out_of_root = self.__github_groups.get_by_team_id(group.id)
                if gh_group_out_of_root is None:
                    self.__github_groups.create(group)
                    group.sync_action = SyncAction.CREATED
                else:
                    self.__github_groups.patch_parent_team(gh_group_out_of_root["id"], group)
                    group.sync_action = SyncAction.PATCHED
                    #TODO UPDATE DO BANCO AQUI?
            else:
                group.sync_action = SyncAction.INSYNC

            logger.log("DEBUG" if group.sync_action == SyncAction.INSYNC else "INFO",
                # f"{self.__client.logkey}"
                f"group={group.name}, "
                f"action={group.sync_action.name}")
        except Exception as err:
            logger.error(
                # f"{self.__client.logkey}"
                f"group={group.name}, "
                f"error={err}")
            raise

    def __sync_gh_to_gws(self):
        #Sync Google Work Space groups and subgroups into GitHub teams

        result = parallel.execute(
            method=self.__sync_from_gh,
            args_list=[{'group': group} for group in self.__sync_data.gh_groups])
        if result.has_errors():
            raise Exception("sync groups failed")

        count = {
            'in-sync': 0,
            'removed': 0
        }

        for group in self.__sync_data.gh_groups:
            if group.sync_action == SyncAction.INSYNC:
                count['in-sync'] += 1
            elif group.sync_action == SyncAction.REMOVED:
                count['removed'] += 1
        # logger.info(f"{self.__client.logkey}in-sync={count['in-sync']:,}")
        # logger.info(f"{self.__client.logkey}removed={count['removed']:,}")

    def __sync_from_gh(self, group):
        try:
            googl_work_space_group = next((g for g in self.__sync_data.gws_groups if g.name == group.name), None)
            group_in_persistence = self.__db.retrieve(group.id)

            if googl_work_space_group is None and group_in_persistence is None:
                self.__github_groups.remove(group)
                group.sync_action = SyncAction.REMOVED
            else:
                #verificar se esse sync acontece mesmo
                group.sync_action = SyncAction.INSYNC
                # self.__db.update() TODO DEVO FAZER UPDATE AQUI DO BANCO?

            logger.log("DEBUG" if group.sync_action == SyncAction.INSYNC else "INFO",
                # f"{self.__client.logkey}"
                f"group={group.name}, "
                f"action={group.sync_action.name}")
        except Exception as err:
            """This is supposed to run with many threads and this log entry helps identifying
            which record had problems. Raising the error only was not enough, since the message
            does not contain the record details
            """
            logger.error(
                # f"{self.__client.logkey}"
                f"group={group.name}, "
                f"error={err}")
            raise
