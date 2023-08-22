from datetime import datetime, timedelta
from typing import Any, List

from shared import Env

from .directory import get_service


class Users:

    def __init__(self):
        self.__service = get_service("users")

    def list(self, custom_schema: str = None, token=None) -> List[Any]:
        """List all users

        :param custom_schema:
            Custom schema name to filter results with

        :param token:
            Google Workspace next page token

        :return list:
            Return list with all users
        """
        resp = self.__service.list(
            customer=Env.CUSTOMER_ID,
            projection='custom',
            customFieldMask=custom_schema,
            pageToken=token
        ).execute()

        # get only users with customSchemas
        users = [u for u in resp.get('users', [])]
        if custom_schema is not None:
            users = [u for u in users if 'customSchemas' in u]

        # get next page
        if resp.get('nextPageToken') is not None:
            users += self.list(
                custom_schema=custom_schema,
                token=resp.get('nextPageToken'))

        return users

    @staticmethod
    def validate_impersonate(user: any) -> List[str]:
        groups = []
        for impersonate in user['customSchemas']['hodor']['active_impersonate']:
            start_time = datetime.fromisoformat(
                ':'.join(impersonate['value'].split(':')[1:]))
            end_time = start_time + timedelta(hours=1)
            if end_time < datetime.now():
                groups.append(impersonate['value'].split(':')[0])

        return groups

    def update_custom_schema(self, group: str, email: str, action: str = 'add') -> None:
        """Update custom schema of user after start or end impersonate

        :param group:
            Group name on Google Workspace
        :param email:
            User email to be updated
        :param action:
            add: group:now() on active_impersonate
            remove: group from active_impersonate
        """
        user = self.__service.get(userKey=email, projection='full').execute()

        if action == 'add':
            values = [{'value': f"{group}:{datetime.now()}"}]
            if 'customSchemas' in user and 'hodor' in user['customSchemas']:
                values += user['customSchemas']['hodor']['active_impersonate']
        elif action == 'remove':
            values = [g for g in user['customSchemas']['hodor']['active_impersonate'] if
                      group not in g['value']]
        else:
            return

        self.__service.update(userKey=user['id'], body={
            'customSchemas': {
                'hodor': {'active_impersonate': values}
            }}).execute()
