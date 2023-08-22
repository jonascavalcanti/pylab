from services.agregator import Agregator
import logging
import sys
from shared.clientapi import ClientApi
from services.sync import Sync
from services.google import Google
from services.github import Github 
from shared import Env
import json


def main():
    logging.basicConfig(level=logging.INFO)

    # ag = Agregator()
    # ag.fon()
    # # ag.import_data()
    # print(ag.receive(7301093))

    #usage db exemples
    # db = DB(filename='hodor.db')
    # db.insert({'id': "dasdad433", 'google_group_name': 'group1', 'github_id': 1, 'github_slug': 'slug1', 'github_name': 'name1'})
    # db.update({'id': "2318dasda", 'google_group_name': 'group3', 'github_id': 3, 'github_slug': 'slug3', 'github_name': 'name3'})

    # for group in db:
    #     print(group)

    

    # sync = Sync()
    # sync.sync('github-users@unico.io')

    # gw = Google(credentials=Env.SA_CRED_INFO)
    # service = gw.search_directory("groups")
    # # TODO migrate that for a lazy function
    # groups = gw.get_groups(service=service)

    # print(json.dumps(groups))

    gh = Github()

    # TODO migrate that for a lazy function
    teams = gh.list_teams(root_team=Env.GH_ROOT_CUSTOM_TEAM)

    print(json.dumps(teams))

if __name__ == '__main__':
    sys.exit(main())
