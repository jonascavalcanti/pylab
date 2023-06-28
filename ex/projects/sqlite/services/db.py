import sqlite3

class DB:
    def __init__(self, **kwargs):
        self.filename = kwargs.get('filename')
        self.table = kwargs.get('table', 'test')

    def sql_do(self, sql, *params):
        self._db.execute(sql, params)
        self._db.commit()

    def insert(self, row):
        self._db.execute('insert into {} (id, google_group_name, github_id, github_slug, github_name) values (?, ?, ?, ?)'.format(self._table), (row['id'], row['google_group_name'], row['github_id'], row['github_slug'], row['github_name']))
        self._db.commit()

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
