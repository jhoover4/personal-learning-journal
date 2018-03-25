from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError

from models import Entry


def title_exists(form, field):
    if Entry.select().where(Entry.title == field.data).exists():
        raise ValidationError("Sorry, posts can't share titles!")


class EntryForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[
            DataRequired(),
            title_exists,
        ])
    time_spent = StringField(
        'Time Spent',
        validators=[
            DataRequired(),
        ])
    learned = StringField(
        'What I Learned',
        validators=[
            DataRequired(),
        ])
    resources = StringField(
        'Resources To Remember',
        validators=[
            DataRequired(),
        ])
    tags = StringField(
        'Tags',
    )
