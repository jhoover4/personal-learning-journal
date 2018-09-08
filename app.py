import re
import string
from flask import Flask, g, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required

import forms
import models

app = Flask(__name__)
app.config.from_object('default_settings')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect(reuse_if_open=True)


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


@app.route('/')
@app.route('/list-entries')
@login_required
def index():
    entries = models.Entry.select().order_by(-models.Entry.date_created)

    for entry in entries:
        tag_query = (models.Tag
                     .select()
                     .join(models.TagList)
                     .join(models.Entry)
                     .where(models.Entry.title == entry.title))

        entry.tags = [tag.name for tag in tag_query]

    return render_template('index.html', entries=entries)


@app.route('/entries/<slug>')
@login_required
def view_entry(slug):
    entry = models.Entry.get(models.Entry.title == slug)

    tag_query = (models.Tag
                 .select()
                 .join(models.TagList)
                 .join(models.Entry)
                 .where(models.Entry.title == entry.title))

    entry.tags = [tag.name for tag in tag_query]

    return render_template('detail.html', entry=entry)


@app.route('/entry', methods=('GET', 'POST'))
@app.route('/entries/edit/<slug>', methods=('GET', 'POST'))
@login_required
def edit_entry(slug=None):
    if slug:
        entry = models.Entry.get(models.Entry.title == string.capwords(slug))
        tag_query = (models.Tag
                     .select()
                     .join(models.TagList)
                     .join(models.Entry)
                     .where(models.Entry.title == entry.title))
        title = 'Edit Entry'
    else:
        entry = models.Entry()
        tag_query = []
        title = 'Add Entry'

    form = forms.EntryForm(obj=entry)
    tags = ", ".join([tag.name.title() for tag in tag_query])

    if form.validate_on_submit():
        form.populate_obj(entry)

        entry.title = string.capwords(form.title.data)
        entry.date_created = form.date_created.data
        entry.time_spent = form.time_spent.data
        entry.learned = form.learned.data
        entry.resources = form.resources.data

        entry.save()

        # Delete all tag lists already associated with model so data can overwrite
        tag_list_query = (models.TagList
                          .select()
                          .join(models.Entry)
                          .where(models.Entry.title == entry.title))
        for ls in tag_list_query:
            ls.delete_instance()

        # Create new tags if needed
        for tag in re.split(r'[\s,]+', form.tags.data):
            tag_name = tag.replace(",", "").title()

            try:
                new_tag = models.Tag.get(models.Tag.name == tag_name)
            except models.DoesNotExist:
                new_tag = models.Tag.create(name=tag_name)

            models.TagList.create(tag=new_tag, entry=entry)

        return redirect(url_for('view_entry', slug=entry.title))

    return render_template('edit.html', form=form, title=title, tags=tags)


@app.route('/entries/delete/<slug>', methods=('GET', 'POST'))
@login_required
def del_entry(slug):
    entry = models.Entry.get(models.Entry.title == slug)

    try:
        models.TagList.delete().where(
            (models.TagList.entry == entry)
        ).execute()
    except models.DoesNotExist:
        pass

    entry.delete_instance()

    return redirect(url_for('index'))


@app.route('/tags/<tag>')
@login_required
def tag_list(tag):
    entries = (models.Entry
               .select()
               .join(models.TagList)
               .join(models.Tag)
               .where(models.Tag.name == tag)).order_by(-models.Entry.date_created)

    return render_template('tag_list.html', entries=entries, tag=tag)


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.username == form.username.data)
        except models.DoesNotExist:
            flash("Your username or password doesn't match!", "error")
        else:
            login_user(user)

            return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
