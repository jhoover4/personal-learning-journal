import re

from flask import Flask, g, render_template, redirect, url_for, request


import forms
import models

DEBUG = True
SECRET = 'ASDF!@#$5%$@#$%fasdf'

app = Flask(__name__)
app.secret_key = SECRET

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


@app.route('/')
@app.route('/list-entries')
def index():
    entries = models.Entry.select()

    for entry in entries:
        tag_query = (models.Tag
               .select()
               .join(models.TagList)
               .join(models.Entry)
               .where(models.Entry.title == entry.title))

        entry.tags = [tag.name for tag in tag_query]

    return render_template('index.html', entries=entries)


@app.route('/entries/<slug>')
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
def edit_entry(slug = None, title=None):
    if slug:
        entry = models.Entry.get(models.Entry.title == slug)
        tags = (models.Tag
               .select()
               .join(models.TagList)
               .join(models.Entry)
               .where(models.Entry.title == entry.title))
        title = 'Edit Entry'
    else:
        entry = models.Entry()
        tags = []
        title = 'Add Entry'
    form = forms.EntryForm(obj=entry)
    if form.validate_on_submit():
        form.populate_obj(entry)

        entry.title = form.title.data.title()
        entry.time_spent = form.time_spent.data
        entry.learned = form.learned.data
        entry.resources = form.resources.data

        entry.save()

        for tag in re.split(r'[\s,]+', form.tags.data):
            try:
                new_tag = models.Tag.get(models.Tag.name == tag)
                models.TagList.create(tag=new_tag, entry=entry)
                tags.append(new_tag)
            except:
                new_tag = models.Tag.create(name=tag)
                models.TagList.create(tag=new_tag, entry=entry)

        return redirect(url_for('view_entry', slug=entry.title))

    return render_template('edit.html', form=form, title=title, tags=tags)


@app.route('/entries/delete/<slug>', methods=('GET', 'POST'))
def del_entry(slug):
    entry = models.Entry.get(models.Entry.title == slug)
    entry.delete_instance()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=DEBUG)
