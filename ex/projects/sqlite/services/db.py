import sqlite3
from inspect import stack
from loguru import logger


class DB:

    def __init__(self, **kwargs):
        self.filename = kwargs.get('filename')
        self.table = kwargs.get('table', 'test')

    def sql_do(self, sql, *params):
        self.__exec(sql, *params)

    def insert(self, row):
        query = 'insert into {} (id, google_group_name, github_id, github_slug, github_name) values (?, ?, ?, ?, ?)'
        self.__exec(query.format(self._table), *(row['id'],
                                                row['google_group_name'],
                                                row['github_id'],
                                                row['github_slug'],
                                                row['github_name']))

    def update(self, row):
        query = 'update {} set google_group_name = ?, github_id = ?, github_slug = ?, github_name = ? where id = ?'
        self.__exec(query.format(self._table), *(row['google_group_name'],
                                                 row['github_id'],
                                                 row['github_slug'],
                                                 row['github_name'],
                                                 row['id']))

    def delete(self, group_id):
        query = 'delete from {} where id = ?'
        self.__exec(query.format(self._table), (group_id))

    def retrieve(self, group_id):
        cursor = self._db.execute('select * from {} where id = ?'.format(self.table), (group_id,))
        return dict(cursor.fetchone())

    def __exec(self, sql, *params):
        # for write and custom commands
        # TODO mult arity/overload
        try:
            self._db.execute(sql, params)
            self._db.commit()
        except sqlite3.IntegrityError as e:
            logger.exception("Error occurred during the operation of {}: {}".format(stack()[1], e))
        

    def __iter__(self):
        # method ref https://peps.python.org/pep-0234/
        query = 'select * from {} order by google_group_name'
        cursor = self._db.execute(query.format(self._table))
        for row in cursor:
            yield dict(row)

    @property
    def filename(self): return self._filename

    @filename.setter
    def filename(self, fn):
        self._filename = fn
        self._db = sqlite3.connect(fn)
        self._db.row_factory = sqlite3.Row

    @filename.deleter
    def filename(self): self.close()

    @property
    def table(self): return self._table
    @table.setter
    def table(self, t): self._table = t
    @table.deleter
    def table(self): self._table = 'test'

    def close(self):
        self._db.close()
        # del self._filename
