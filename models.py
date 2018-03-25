from datetime import datetime
from peewee import *

DATABASE = SqliteDatabase('entries.db')


class BaseModel(Model):
    class Meta:
        database = DATABASE


class Tag(BaseModel):
    """For associating different entries by tag."""

    name = CharField(unique=True)

    class Meta:
        order_by = 'name'


class Entry(BaseModel):
    """title, date, time spent, what you learned, and resources to remember."""

    date_created = DateTimeField(default=datetime.now)
    title = CharField(unique=True)
    time_spent = IntegerField()  # minutes
    learned = TextField()
    resources = TextField()

    class Meta:
        order_by = ('-date_created',)


class TagList(BaseModel):
    """For many to many relationship between tags and entries."""

    tag = ForeignKeyField(Tag)
    entry = ForeignKeyField(Entry)


class User(BaseModel):
    """Protection for editing entries."""

    date_created = DateTimeField(default=datetime.now)
    username = CharField(unique=True)
    password = CharField(max_length=100)


def initialize_db():
    DATABASE.connect()
    DATABASE.create_tables([Entry, User, Tag, TagList], safe=True)
    DATABASE.close()
