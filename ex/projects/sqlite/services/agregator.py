from services.db import DB
from services.group import Group
from services.github import Github 
from services.google import Google
from shared import Env

class Agregator:

    def __init__(self):

        self.gw = Google(credentials=Env.SA_CRED_INFO)
        self.service = self.gw.search_directory("groups")
        #TODO migrate that for a lazy function
        self.groups = self.gw.get_groups(service=self.service)

        self.gh = Github()
        #TODO migrate that for a lazy function
        self.teams = self.gh.list_teams(root_team=Env.GH_ROOT_TEAM)

        self.db = DB(filename="hodor.db")
        self.group = Group

    def import_data(self):
        for github in self.group.from_gh_teams(self.teams):
            for google in self.group.from_gws_groups(self.groups):
                if github.name == google.name:
                    self.db.insert({'id': google.id,
                                    'google_group_name': google.name,
                                    'github_id': github.id,
                                    'github_slug': github.name,
                                    'github_name': github.name})
                    continue

    def receive(self, id):
        return self.db.retrieve(id)


