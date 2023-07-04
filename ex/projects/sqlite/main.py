from services.google import Google
from services.agregator import Agregator
from shared import Env
import logging
import sys
import json


teams = [
    {
        "id": 1,
        "node_id": "MDQ6VGVhbTE=",
        "url": "https://api.github.com/teams/1",
        "html_url": "https://github.com/orgs/github/teams/justice-league",
        "name": "trab",
        "slug": "trab",
        "description": "A great team.",
        "privacy": "closed",
        "notification_setting": "notifications_enabled",
        "permission": "admin",
        "members_url": "https://api.github.com/teams/1/members{/member}",
        "repositories_url": "https://api.github.com/teams/1/repos",
    },
    {
        "id": 2,
        "node_id": "MDQ6VGVhbTE=",
        "url": "https://api.github.com/teams/1",
        "html_url": "https://github.com/orgs/github/teams/justice-league",
        "name": "fon",
        "slug": "fon",
        "description": "A great team.",
        "privacy": "closed",
        "notification_setting": "notifications_enabled",
        "permission": "admin",
        "members_url": "https://api.github.com/teams/1/members{/member}",
        "repositories_url": "https://api.github.com/teams/1/repos",
    }
]


def main():
    logging.basicConfig(level=logging.INFO)

    g = Google(credentials=Env.SA_CRED_INFO)

    service = g.search_directory("groups")

    resp = service.list(
            customer=Env.CUSTOMER_ID
        ).execute()

    groups = json.loads(json.dumps(resp["groups"]))
    
    ag = Agregator()
    ag.import_data(teams, groups)
    print(ag.receive("025b2l0r4fnu38p"))

    db = DB(filename='hodor.db')
    db.insert({'id': "dasdad433", 'google_group_name': 'group1', 'github_id': 1, 'github_slug': 'slug1', 'github_name': 'name1'})
    db.insert({'id': "dasdad433", 'google_group_name': 'group2', 'github_id': 2, 'github_slug': 'slug2', 'github_name': 'name2'})
    db.update({'id': "2318dasda", 'google_group_name': 'group3', 'github_id': 3, 'github_slug': 'slug3', 'github_name': 'name3'})
    db.update({'id': "123dsaref", 'google_group_name': 'group4', 'github_id': 4, 'github_slug': 'slug4', 'github_name': 'name4'})

    for group in db:
        print(group)


if __name__ == '__main__':
    sys.exit(main())
