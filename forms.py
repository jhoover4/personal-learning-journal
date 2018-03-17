from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError

from models import Entry


def title_exists(form, field):
    if Entry.select().where(Entry.title == field.data).exists():
        raise ValidationError("Sorry, posts can't share titles!")


class EntryForm(Form):
    title = StringField(
        'title',
        validators=[
            DataRequired(),
            title_exists,
        ])
    time_spent = StringField(
        'timeSpent',
        validators=[
            DataRequired(),
        ])
    learned = StringField('whatILearned')
    resources = StringField('ResourcesToRemember')
