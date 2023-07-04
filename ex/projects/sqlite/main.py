from services.google import Google
from services.agregator import Agregator
from services.github import Github
from shared import Env
import logging
import sys
import json


def main():
    logging.basicConfig(level=logging.INFO)

    gw = Google(credentials=Env.SA_CRED_INFO)
    service = gw.search_directory("groups")
    resp = service.list(
            customer=Env.CUSTOMER_ID
        ).execute()
    get_groups = resp["groups"]

    
    gh = Github()
    get_tems = gh.get(path=f"/orgs/{Env.GH_ORG}/teams")


    # print("google groups", groups)
    # print("github teams", teams)

    ag = Agregator()
    ag.import_data(get_tems, get_groups)
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
