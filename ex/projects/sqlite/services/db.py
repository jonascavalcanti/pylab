import sqlite3
import json
from sqlite3 import Error

class SQLite:
    def __init__(self, db_file: str) -> None:
        self.db_file = db_file
        self.__sql_inicial_load()
    
    def get_connection(self):
        """ create a database connection to the SQLite database
        specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
        except Error as e:
            print(e)

        return conn
    
    def __sql_inicial_load(self):
        sql = """ CREATE TABLE IF NOT EXISTS groups (
                                        id varchar(3) PRIMARY KEY,
                                        google_workspace_name text NOT NULL,
                                        github_id interger NOT NULL,
                                        github_slug text NOT NULL,
                                        github_name text NOT NULL
                                    ); """
        conn = self.get_connection()
        self.__create_table(conn, sql)
        
    def __create_table(self, conn, sql: str):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param sql: a CREATE TABLE statement
        :return:
        """
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
        except Error as e:
            print(e)

    def insert(self, conn, table: str, data: map):
        sql = "INSERT INTO " + table + " VALUES (?, ?)"

        try:
            cursor = conn.cursor()
            cursor.execute(sql, [data['id'], json.dumps(data)])
            conn.commit()
        except Error as e:
            print(e)
            