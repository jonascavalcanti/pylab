
import os.path
import json
from shared import Env
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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
                                                    subject=Env.SA_SUBJECT)
            
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
         
