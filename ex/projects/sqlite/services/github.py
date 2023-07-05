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

    def get_by_team_name(self, team_name: str):
        try:
            return self.get(path=f"/orgs/{Env.GH_ORG}/teams/{team_name}")
        except Exception as ex:
            if "HTTP 404/" in str(ex):
                return None
            raise
