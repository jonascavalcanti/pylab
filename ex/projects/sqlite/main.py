from services.google import Google
from services.agregator import Agregator
from services.github import Github
from shared import Env
import logging
import sys


def main():
    logging.basicConfig(level=logging.INFO)

    gw = Google(credentials=Env.SA_CRED_INFO)
    service = gw.search_directory("groups")
    groups = gw.get_groups(service=service)
    
    # for group in groups:
    #     print(group["name"])
    
    gh = Github()
    teams = gh.list_teams(root_team=Env.GH_ROOT_TEAM)
    
    # for team in teams:
    #     print(team["name"])
   
    # print("google groups", groups)
    # print("github teams", teams)

    ag = Agregator()
    ag.import_data(teams, groups)
    print(ag.receive("048pi1tg4f82ygq"))

    # db = DB(filename='hodor.db')
    # db.insert({'id': "dasdad433", 'google_group_name': 'group1', 'github_id': 1, 'github_slug': 'slug1', 'github_name': 'name1'})
    # db.insert({'id': "dasdad433", 'google_group_name': 'group2', 'github_id': 2, 'github_slug': 'slug2', 'github_name': 'name2'})
    # db.update({'id': "2318dasda", 'google_group_name': 'group3', 'github_id': 3, 'github_slug': 'slug3', 'github_name': 'name3'})
    # db.update({'id': "123dsaref", 'google_group_name': 'group4', 'github_id': 4, 'github_slug': 'slug4', 'github_name': 'name4'})

    # for group in db:
    #     print(group)


if __name__ == '__main__':
    sys.exit(main())
