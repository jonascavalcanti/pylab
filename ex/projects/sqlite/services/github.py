from typing import Optional
from shared.clientapi import ClientApi
from .syncdata import SyncData 
from shared import Env

import json

class Github(ClientApi):

    def __init__(self):
        Env.validate_envs(["API_GH_ENDPOINT",
                           "API_GH_SYNC_GROUP",
                           "API_GH_SECRET"])

        super(Github, self).__init__(
                Env.API_GH_ENDPOINT,
                {'Authorization': f"Bearer {Env.API_GH_SECRET}"}
            )

        self.__sync_data = SyncData()
        self.__client = ClientApi
        self.__gh_org = Env.GH_ORG
        
    def list_teams(self, root_team=None, page=1, teams=None):
        if teams is None:
            teams = []
    
        url_path = f"/orgs/{Env.GH_ORG}/teams"

        if root_team is not None:
            root_team_id = self.get_by_team_name(root_team)["id"]
            url_path = f"/orgs/{Env.GH_ORG}/team/{root_team_id}/teams"
        
        current_page_teams = self.get(
                path=url_path,
                params={"per_page": 100, "page": page})
        
        if len(current_page_teams) > 0:
            teams.extend(current_page_teams)
            page += 1
            if root_team is not None:
                return self.list_teams(root_team, page, teams)
            else:
                return self.list_teams(None, page, teams)
        else:
            return teams
        
    # def list_teams(self, root_team_id: str, page=1, teams=None):
    #     if teams is None:
    #         teams = []

    #     current_page_teams = self.get(
    #         path=f"/orgs/{self.__gh_org}/team/{root_team_id}/teams",
    #         params={"per_page": 100, "page": page})

    #     if len(current_page_teams) > 0:
    #         teams.extend(current_page_teams)
    #         page += 1
    #         return self.list_teams(root_team_id, page, teams)
    #     else:
    #         return teams

    def get_by_team_name(self, team_name: str) -> Optional[dict]:
        try:
            return self.get(path=f"/orgs/{Env.GH_ORG}/teams/{team_name}")
        except Exception as ex:
            if "HTTP 404/" in str(ex):
                return None
            raise

    
    def get_by_team_id(self, team_id: str):
        try:
            return self.get(path=f"/organizations/{Env.GH_ORG_ID}/teams/{team_id}")
        except Exception as ex:
            if "HTTP 404/" in str(ex):
                return None
            raise

    def create(self, group):
        if Env.DRY_RUN:
            return
        return self.__client.post(path=f"/orgs/{self.__gh_org}/teams", data=json.dumps(
            {
                "name": group.name,
                "privacy": "closed",
                "parent_team_id":
                self.__sync_data.root_gh_team_id if group.pattern_verified
                    else self.__sync_data.root_custom_gh_team_id
            }))

    def patch_parent_team(self, team_id, team):
        if Env.DRY_RUN:
            return
        self.patch(path=f"/orgs/{self.__gh_org}/team/{team_id}", data=json.dumps(
            {"parent_team_id": self.__sync_data.root_gh_team_id if team.pattern_verified
                else self.__sync_data.root_custom_gh_team_id}))

    def update_team(self, team_id, changes: dict):
        if Env.DRY_RUN:
            return
        self.patch(path=f"/orgs/{self.__gh_org}/team/{team_id}", data=json.dumps(
            changes))

    def remove(self, group):
        if Env.DRY_RUN:
            return
        self.delete(path=f"/orgs/{self.__gh_org}/teams/{group.name}")
