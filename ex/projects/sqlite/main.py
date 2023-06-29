from services.db import DB
import sys

db = DB(filename="./hodor.db", table='groups')


def main():

    # m = {
    #     "id": 2211596,
    #     "google_workspace_name": "tribe-people",
    #     "github_id": 1000,
    #     "github_slug": "tribe-people",
    #     "github_name": "tribe-people"
    #     }

    # TODO colar essas funçoes em um outro metodo que vai cuidar das coisas do hodor
    db.sql_do("""CREATE TABLE IF NOT EXISTS groups (
                                            id varchar(3) PRIMARY KEY,
                                            google_group_name text NOT NULL,
                                            github_id interger NOT NULL,
                                            github_slug text NOT NULL,
                                            github_name text NOT NULL
                                        );
        """)

    db.insert(dict(id = 123,
                google_group_name='francisco',
                github_id=321,
                github_slug='francisco',
                github_name='francisco'))

    print('actual', db.retrieve(123))

    print('after update', db.update(dict(id=123,
                    google_group_name='jonas o mestre dos magos',
                    github_id=321,
                    github_slug='jonas_o_mestre_dos_magos',
                    github_name='jonas o mestre dos magos')))

    print('actual', db.retrieve(123))


if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit
