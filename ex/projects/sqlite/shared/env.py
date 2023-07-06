import base64
import os.path


class Env:
    # APP
    DRY_RUN = os.getenv('DRY_RUN', '0') == '1'
    LOGURU_LEVEL = os.getenv('LOGURU_LEVEL', 'DEBUG')
    API_SLEEP_TIME = int(os.getenv('API_SLEEP_TIME', '30'))
    API_MAX_ATTEMPTS = int(os.getenv('API_MAX_ATTEMPTS', '10'))
    URL = os.getenv('URL', '')
    PROJECT = os.getenv('PROJECT', '')
    REGION = os.getenv('REGION', 'us-east1')

    # GH
    API_GH_ENDPOINT = os.getenv('API_GH_ENDPOINT', '')
    API_GH_SECRET = os.getenv('API_GH_SECRET', '')
    API_GH_SYNC_GROUP = os.getenv('API_GH_SYNC_GROUP', '')
    GH_ROOT_TEAM = os.getenv('GH_ROOT_TEAM', '')
    GH_ROOT_CUSTOM_TEAM = os.getenv('GH_ROOT_CUSTOM_TEAM', '')
    GH_ORG = os.getenv('GH_ORG', '')

    # GWS
    CUSTOMER_ID = os.getenv('CUSTOMER_ID', '')
    SA_SUBJECT = os.getenv('SA_SUBJECT', '')
    SA_CRED_INFO = base64.b64decode(os.getenv('SA_CRED_B64')).decode('utf-8')

    # SLACK
    SLACK_TOKEN = os.getenv('SLACK_TOKEN', '')
    SLACK_SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET', '')

    # Machine
    MAX_WORKERS = os.getenv('MAX_WORKERS', 1)

    @staticmethod
    def validate_envs(env_names):
        errors = [n for n in env_names if len(getattr(Env, n)) == 0]
        if len(errors) == 0:
            return

        raise ValueError(f"Required environment variables are not set: {', '.join(errors)}.")
