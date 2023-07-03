from services.db import DB
from services.agregator import Agregator
import logging
import sys

groups = [
    {
        "id": 123,
        "email": "trab",
        "name": "trab",
        "description": "trab",
        "adminCreated": "false",
        "directMembersCount": "traba",
        "kind": "traba",
        "etag": "traba",
        "aliases": [
            "trab"
        ],
        "nonEditableAliases": [
            "trab"
        ]
    },
    {
        "id": 456,
        "email": "fon",
        "name": "fon",
        "description": "fon",
        "adminCreated": "true",
        "directMembersCount": "fon",
        "kind": "fon",
        "etag": "fon",
        "aliases": [
            "fon"
        ],
        "nonEditableAliases": [
            "fon"
        ]
    }
]

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

    ag = Agregator()
    ag.import_data(teams, groups, )
    print(ag.receive(456))

    # db = DB(filename='hodor.db')
    # db.insert({'id': 1, 'google_group_name': 'group1', 'github_id': 1, 'github_slug': 'slug1', 'github_name': 'name1'})
    # db.insert({'id': 2, 'google_group_name': 'group2', 'github_id': 2, 'github_slug': 'slug2', 'github_name': 'name2'})
    # db.update({'id': 1, 'google_group_name': 'group3', 'github_id': 3, 'github_slug': 'slug3', 'github_name': 'name3'})
    # db.update({'id': 3, 'google_group_name': 'group4', 'github_id': 4, 'github_slug': 'slug4', 'github_name': 'name4'})

    # for group in db:
    #     print(group)


if __name__ == '__main__':
    sys.exit(main())
