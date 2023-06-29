from services.db import DB
import sys

def main():

    db = DB(filename="./hodor.db", table='groups')
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

    db.update(dict(id=123,
                   google_group_name='jonas o mestre dos magos',
                   github_id=321,
                   github_slug='jonas_o_mestre_dos_magos',
                   github_name='jonas o mestre dos magos'))

    print('after update', db.retrieve(123))

if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit
