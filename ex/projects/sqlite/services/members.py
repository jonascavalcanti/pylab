from typing import List

from .directory import get_service
from .exceptions import MemberAlreadyInGroup, MemberNotInGroup, MemberRequireApproval
from .users import Users
from .google import Google, Groups

class Members:

    def __init__(self):
        self.__service = get_service("members")
        self.__user = Users()

    def __get_members(self, group: str, role: str) -> List[str]:
        """Get list of members by role and return list of emails

        :param group:
            Group name on Google Workspace
        :param role:
            Member group role on Google Workspace
        :return:
            list of emails
        """
        results = self.__service.list(groupKey=group, roles=role).execute()
        emails = map(lambda m: m['email'], results.get('members', []))
        return list(emails)

    def list_users_by_group(self, group: str):
        """Get list of all users from a group filtering by member ids

        :param group:
            Group name on Google Workspace
        """
        users = self.__user.list()
        user_ids = self.get_group_indirect_members(group)
        users = [user for user in users if user['id'] in user_ids]
        return users

    def list_sub_groups(self, group, prefixes_allow="", suffixes_allow="", email_suffixes_allow=""):
        gws_groups = Groups().list()
        group_ids = self.get_group_indirect_members(group)
        gws_groups = [
            gws_group
            for gws_group
            in gws_groups
            if (gws_group['id'] in group_ids and
                gws_group['email'].split("@")[0].lower().startswith(prefixes_allow) and
                gws_group['email'].split("@")[0].lower().endswith(suffixes_allow) and
                gws_group['email'].lower().endswith(email_suffixes_allow))]
        return gws_groups

    def get_group_members(self, group: str, token=None) -> List[str]:
        """Get list of all direct members of a group

        :param group:
            Group name on Google Workspace
        :param token:
            Google Workspace next page token
        :return:
            list of user IDs
        """
        results = self.__service.list(
            groupKey=group,
            includeDerivedMembership=False,
            pageToken=token
        ).execute()

        if 'members' not in results:
            return []

        members = [
            member['id']
            for member
            in results['members']]

        if 'nextPageToken' in results:
            members += self.get_group_members(
                group=group,
                token=results['nextPageToken'])

        return members

    def get_group_indirect_members(self, group: str, token=None) -> List[str]:
        """Get list of all members of a groups, direct and indirect

        :param group:
            Group name on Google Workspace
        :param token:
            Google Workspace next page token
        :return:
            list of user IDs
        """
        results = self.__service.list(
            groupKey=group,
            includeDerivedMembership=True,
            pageToken=token
        ).execute()

        if 'members' not in results:
            return []

        members = [
            member['id']
            for member
            in results['members']]

        if 'nextPageToken' in results:
            members += self.get_group_indirect_members(
                group=group,
                token=results['nextPageToken'])

        return members

    def get_group_admins(self, group: str) -> List[str]:
        """Get list of owners/managers and return list of emails

        :param group:
            Group name on Google Workspace
        :return:
            list of emails
        """
        owners = self.__get_members(group, "OWNER")
        managers = self.__get_members(group, "MANAGER")
        return owners + managers

    def grant_full_access(self, group: str, email: str, manager_approved=False) -> str:
        """Put user on full access group

        :param group:
            Group name on Google Workspace
        :param email:
            User email
        :param manager_approved:
            Boolean to set if manager has approved users outside group to get full access
        :return:
            True if user has been added with success
        """
        if not manager_approved:
            results = self.__service.hasMember(groupKey=group, memberKey=email).execute()
            if not results.get('isMember', False):
                raise MemberNotInGroup(email, group)
            member = self.__service.get(groupKey=group, memberKey=email).execute()
            if member.get('role') == 'MEMBER':
                raise MemberRequireApproval(email, group)

            admins = self.get_group_admins(group=group)
            if member.get('email') not in admins:
                raise MemberRequireApproval(email, group)

        full_group = group.replace('@', '-full@')
        results = self.__service.hasMember(groupKey=full_group, memberKey=email).execute()
        if results.get('isMember', False):
            raise MemberAlreadyInGroup(email, full_group)

        self.add_in_group(full_group, email)

        return full_group

    def add_in_group(self, group: str, email: str) -> None:
        """Add user in Google Workspace group

        :param group:
            Group name on Google Workspace
        :param email:
            User email to be add
        :return:
            Return True when status is active
        """
        results = self.__service.hasMember(groupKey=group, memberKey=email).execute()
        if results.get('isMember', False):
            raise MemberAlreadyInGroup(email, group)

        self.__service.insert(groupKey=group, body={'email': email, 'role': 'MEMBER'}).execute()

        self.__user.update_custom_schema(group, email)

    def remove_from_group(self, group: str, email: str) -> None:
        """Remove user from group

        :param group:
            Group name on Google Workspace
        :param email:
            User email to be removed
        """
        results = self.__service.hasMember(groupKey=group, memberKey=email).execute()
        if not results.get('isMember', False):
            raise MemberNotInGroup(email, group)

        self.__service.delete(groupKey=group, memberKey=email).execute()

        self.__user.update_custom_schema(group, email, 'remove')
