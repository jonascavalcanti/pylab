from shared.clientapi import ClientApi
from shared import Env


class Github(ClientApi):

    def __init__(self):
        Env.validate_envs(["API_GH_ENDPOINT",
                           "API_GH_SYNC_GROUP",
                           "API_GH_SECRET"])
        
        super(Github, self).__init__(
                Env.API_GH_ENDPOINT,
                {'Authorization': f"Bearer {Env.API_GH_SECRET}"}
            )
    
