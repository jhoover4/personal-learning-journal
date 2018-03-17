from peewee import *

DATABASE = SqliteDatabase('sql.db')


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Urls, ImageSearches], safe=True)
    DATABASE.close()