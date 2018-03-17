from datetime import datetime
from peewee import *

DATABASE = SqliteDatabase('sql.db')


class Entry(Model):
    """title, date, time spent, what you learned, and resources to remember"""

    date_created = DateTimeField(default=datetime.now)
    title = CharField(unique=True)
    time_spent = IntegerField() # minutes
    learned = TextField()
    resources = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-date_created',)

class User(Model):
    date_created = DateTimeField(default=datetime.datetime.now)
    username = CharField(unique=True)
    password = CharField(max_length=100)

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry, User], safe=True)
    DATABASE.close()
