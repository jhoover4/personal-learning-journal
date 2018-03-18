from datetime import datetime
from peewee import *

DATABASE = SqliteDatabase('entries.db')

class Tag(Model):
    """For associating different entries by tag."""
    name = CharField()

class Entry(Model):
    """title, date, time spent, what you learned, and resources to remember."""

    date_created = DateTimeField(default=datetime.now)
    title = CharField(unique=True)
    time_spent = IntegerField()  # minutes
    learned = TextField()
    resources = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-date_created',)

class Course(Model):
    name = CharField()

class TagList(Model):
    """For many to many relationship between tags and entries."""

    student = ForeignKeyField(Tag)
    course = ForeignKeyField(Entry)

class User(Model):
    """Protection for editing entries"""

    date_created = DateTimeField(default=datetime.now)
    username = CharField(unique=True)
    password = CharField(max_length=100)


def initialize_db():
    DATABASE.connect()
    DATABASE.create_tables([Entry, User], safe=True)
    DATABASE.close()
