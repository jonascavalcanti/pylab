from services.db import DB

class Agregator:

    def __init__(self, **kwargs):
        #variables
        # self.gh_groups = kwargs.get('github_groups')
        # self.g_groups = kwargs.get('google_groups')

        self.db = DB(filename="hodor.db")

    def import_data(self, gh_groups, g_groups):

        for google in g_groups:
            for github in gh_groups:
                if google["name"] == github["name"]:
                    self.db.insert({'id': google["id"],
                                    'google_group_name': google["name"],
                                    'github_id': github["id"],
                                    'github_slug': github["slug"],
                                    'github_name': github["id"]})
                    continue

    def receive(self, id):
        return self.db.retrieve(id)

