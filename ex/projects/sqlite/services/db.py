import logging
from sqlalchemy import create_engine, inspect, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData, Column
from sqlalchemy.exc import SQLAlchemyError

class DB:
    def __init__(self, **kwargs):
        self.filename = kwargs.get('filename')
        self.table = kwargs.get('table', 'groups')

        self.engine = create_engine('sqlite:///{}'.format(self.filename))
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        self.metadata = MetaData()
        self.groups_table = self.create_groups_table()

    def create_groups_table(self):
        inspector = inspect(self.engine)
        if not inspector.has_table('groups'):
            self.groups_table = Table(
                'groups',
                self.metadata,
                Column('id', String, primary_key=True),
                Column('google_group_name', String, nullable=False),
                Column('github_id', Integer, nullable=False),
                Column('github_slug', String, nullable=False),
                Column('github_name', String, nullable=False)
            )
            self.groups_table.create(self.engine)
            logging.info('Table "groups" successfully created..')
            return self.groups_table
        else:
            self.groups_table = Table('groups', self.metadata, autoload_with=self.engine)
            logging.info('Table "groups" already exists. Using existing table..')

            return self.groups_table

    def insert(self, row):
        existing_record = self.retrieve(row['id'])
        if existing_record:
            logging.info('Record with ID {} already exists. skipping insertion.'.format(row['id']))
            return

        try:
            new_record = self.groups_table.insert().values(
                id=row['id'],
                google_group_name=row['google_group_name'],
                github_id=row['github_id'],
                github_slug=row['github_slug'],
                github_name=row['github_name']
            )
            self.session.execute(new_record)
            self.session.commit()
            logging.info('Record inserted successfully.')
        except SQLAlchemyError as e:
            logging.error('Error inserting record: {}'.format(str(e)))
            self.session.rollback()
            raise

    def update(self, row):
        existing_record = self.retrieve(row['id'])
        if not existing_record:
            logging.info('Record with ID {} does not exist. skipping update.'.format(row['id']))
            return

        try:
            update_record = self.groups_table.update().where(
                self.groups_table.c.id == row['id']
            ).values(
                google_group_name=row['google_group_name'],
                github_id=row['github_id'],
                github_slug=row['github_slug'],
                github_name=row['github_name']
            )
            self.session.execute(update_record)
            self.session.commit()
            logging.info('Registration updated successfully.')
        except SQLAlchemyError as e:
            logging.error('Error updating record: {}'.format(str(e)))
            self.session.rollback()
            raise

    def delete(self, group_id):
        try:
            delete_record = self.groups_table.delete().where(
                self.groups_table.c.id == group_id
            )
            self.session.execute(delete_record)
            self.session.commit()
        except SQLAlchemyError as e:
            logging.error('Error deleting record: {}'.format(str(e)))
            self.session.rollback()
            raise

    def retrieve(self, group_id):
        try:
            query = self.groups_table.select().where(
                self.groups_table.columns.id == group_id
            )
            result = self.session.execute(query)
            record = result.fetchone()
            if record:
                columns = result.keys()
                return dict(zip(columns, record))
            else:
                logging.info('Record with ID {} not found.'.format(group_id))
                return None
        except SQLAlchemyError as e:
            logging.error('Error retrieving record: {}'.format(str(e)))
            raise

    def __iter__(self):
        try:
            query = self.groups_table.select().order_by(
                self.groups_table.columns.google_group_name
            )
            result = self.session.execute(query)
            for record in result:
                colums = result.keys()
                yield dict(zip(colums, record))
        except SQLAlchemyError as e:
            logging.error('Error when iterating records: {}'.format(str(e)))
            raise

