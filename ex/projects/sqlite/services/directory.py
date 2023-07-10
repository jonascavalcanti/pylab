import json
import os
from typing import Any

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from shared import Env


def get_service(service_name: str) -> Any:
    """Return instance of service

    :param service_name:
        Name of directory_v1 service
    :return:
        Instance of service
    """
    credentials = Credentials.from_service_account_info(
        info=json.loads(Env.SA_CRED_INFO),
        scopes=['https://www.googleapis.com/auth/admin.directory.user',
                'https://www.googleapis.com/auth/admin.directory.group',
                'https://www.googleapis.com/auth/admin.directory.group.member',
                'https://www.googleapis.com/auth/admin.directory.userschema'],
        subject=os.environ.get('SA_SUBJECT'))

    svc = build('admin', 'directory_v1', credentials=credentials)
    if service_name == 'groups':
        return svc.groups()
    if service_name == 'members':
        return svc.members()
    if service_name == 'schemas':
        return svc.schemas()
    if service_name == 'users':
        return svc.users()

    raise Exception(f"Service with name [{service_name}] does not exist.")
