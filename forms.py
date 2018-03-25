from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField
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
            # title_exists,
        ])
    date_created = DateField(
        'Date',
        format="%m/%d/%Y",
        validators=[
            DataRequired(),
        ])
    time_spent = StringField(
        'Time Spent (In Hours)',
        validators=[
            DataRequired(),
        ])
    learned = TextAreaField(
        'What I Learned',
        validators=[
            DataRequired(),
        ])
    resources = TextAreaField(
        'Resources To Remember',
        validators=[
            DataRequired(),
        ])
    tags = StringField(
        'Tags',
    )
