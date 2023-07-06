from services.google import Google
from services.agregator import Agregator
from services.github import Github
from shared import Env
import logging
import sys


def main():
    logging.basicConfig(level=logging.INFO)

    ag = Agregator()
    # ag.import_data()
    print(ag.receive(7301093))

    #usage db exemples
    # db = DB(filename='hodor.db')
    # db.insert({'id': "dasdad433", 'google_group_name': 'group1', 'github_id': 1, 'github_slug': 'slug1', 'github_name': 'name1'})
    # db.update({'id': "2318dasda", 'google_group_name': 'group3', 'github_id': 3, 'github_slug': 'slug3', 'github_name': 'name3'})

    # for group in db:
    #     print(group)


if __name__ == '__main__':
    sys.exit(main())
