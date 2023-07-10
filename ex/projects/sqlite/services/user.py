from __future__ import annotations

from typing import List

from shared import Const, parallel, SyncAction


class User:
    def __init__(
            self,
            external_id: str,
            email: str,
            given_name: str,
            family_name: str,
            display_name: str,
            active: bool,
            gh_username: str,
    ):
        self.id = ''
        self.external_id = external_id
        self.username = email
        self.given_name = given_name
        self.family_name = family_name
        self.display_name = display_name
        self.email = email
        self.active = active
        self.gh_username = gh_username
        self.sync_action = SyncAction.NONE

    @staticmethod
    def from_gws(gws_user: dict, username_emails: [dict] = None) -> User:
        """Creates a new instance based on GWS-shaped data

        :param gws_user:
            Dictionary containing GWS-shaped user data
        :param username_emails:
            List of github usernames and org emails
        """
        email = [e for e in gws_user['emails'] if str(e['address']).endswith(Const.EMAIL_SUFFIX)][0]['address']
        given_name = gws_user['name']['givenName']
        family_name = gws_user['name']['familyName']
        display_name = f"{given_name} {family_name}"
        gh_username = ""
        if username_emails is not None:
            gh_username = next((u["username"] for u in username_emails if u["email"] == email), "")

        return User(
            external_id=gws_user['id'],
            email=email,
            given_name=given_name,
            family_name=family_name,
            display_name=display_name,
            active=(not gws_user['suspended']),
            gh_username=gh_username)

    @staticmethod
    def from_gws_list(gws_users: List[dict], username_emails: List[dict] = None) -> List[User]:
        """Creates a new instance list based on GWS-shaped data

        :param gws_users:
            Dictionary list containing GWS-shaped users data
        :param username_emails:
            List of github usernames and org emails
        """
        result = parallel.execute(
            method=User.from_gws,
            args_list=[{'gws_user': gws_user, "username_emails": username_emails} for gws_user in gws_users])

        if result.has_errors():
            raise Exception('User data normalization failed.')

        users = []
        for result in result.results:
            users.append(result)

        return users

    @staticmethod
    def from_gh(gh_user: dict, username_emails: List[dict] = None) -> User:
        """Creates a new instance based on GWS-shaped data

        :param gh_user:
            Dictionary containing GWS-shaped user data
        :param username_emails:
            List of github usernames and org emails
        """
        email = ""
        if username_emails is not None:
            email = next((u["email"] for u in username_emails if u["username"] == gh_user["login"]), "")
        gh_username = gh_user["login"]

        return User(
            external_id=gh_user['id'],
            email=email,
            given_name="",
            family_name="",
            display_name="",
            active=True,
            gh_username=gh_username)

    @staticmethod
    def from_gh_list(gh_users: List[dict], username_emails: List[dict]) -> List[User]:
        """Creates a new instance list based on GWS-shaped data

        :param gh_users:
            Dictionary list containing GWS-shaped users data
        :param username_emails:
            List of github usernames and org emails
        """
        result = parallel.execute(
            method=User.from_gh,
            args_list=[{'gh_user': gh_user, 'username_emails': username_emails} for gh_user in gh_users])

        if result.has_errors():
            raise Exception('User data normalization failed.')

        users = []
        for result in result.results:
            users.append(result)

        return users
