from typing import List, Any
import json
from shared import Env
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


import re
from typing import List, Any

from shared import Env

from .directory import get_service


def get_group_from_message(message: str) -> str:
    """Extract group name from slack approval message

    :param message:
        Slack approval message
    :return:
        Group name
    """
    match = re.search(r'\*(.*?)\*', message)

    return match.group(1)


class Groups:
    def __init__(self):
        self.__service = get_service("groups")

    def exists(self, group=None) -> bool:
        """Verify if group exists on Google Workspace

        :param group:
            Google group name

        :return:
            Boolean
        """
        try:
            response = self.__service.get(groupKey=group).execute()

            return response.get('email', "") == group
        except:
            return False

    def list(self, token=None) -> List[Any]:
        """List all groups

        :param token:
            Google Workspace next page token

        :return list:
            Return list with all users
        """
        resp = self.__service.list(
            customer=Env.CUSTOMER_ID,
            pageToken=token
        ).execute()

        # get only users with customSchemas
        groups = [g for g in resp.get('groups', [])]

        # get next page
        if resp.get('nextPageToken') is not None:
            groups += self.list(
                token=resp.get('nextPageToken'))

        return groups

scopes = ['https://www.googleapis.com/auth/admin.directory.user',
        'https://www.googleapis.com/auth/admin.directory.group',
        'https://www.googleapis.com/auth/admin.directory.group.member',
        'https://www.googleapis.com/auth/admin.directory.userschema']


class Google:

    def __init__(self, **kwargs):
        self.__credentials = kwargs.get('credentials')

    def search_directory(self, service_name: str):

        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.

        try:
    
            creds = service_account.Credentials.from_service_account_info(
                                        info=json.loads(self.__credentials),
                                        scopes=scopes,
                                        subject=Env.SA_SUBJECT
                                        )
            
            svc = build('admin', 'directory_v1', credentials=creds)
            
            action = {
                'groups': svc.groups(),
                'members': svc.members(),
                'schemas': svc.schemas(),
                'users': svc.users(),
            }

            return action[service_name]
        except HttpError as err:
            print(err)
 
    def get_groups(self, service=None, token=None) -> List[Any]:
        """List all groups

        :param token:
            Google Workspace next page token

        :return list:
            Return list with all users
        """
        resp = service.list(
            customer=Env.CUSTOMER_ID,
            pageToken=token
        ).execute()

        # get only users with customSchemas
        groups = [g for g in resp.get('groups', [])]
    
        # get next page
        if resp.get('nextPageToken') is not None:
            groups += self.get_groups(service=service,
                                      token=resp.get('nextPageToken'))

        return groups

