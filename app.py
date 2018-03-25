import re

from flask import Flask, g, render_template, redirect, url_for

import forms
import models

DEBUG = True
SECRET = 'ASDF!@#$5%$@#$%fasdf'

app = Flask(__name__)
app.secret_key = SECRET


# TODO: Implement User Auth
# TODO: Implement Tag-list delete
# TODO: Fix title capitlization on conjunctions

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
def edit_entry(slug=None):
    if slug:
        entry = models.Entry.get(models.Entry.title == slug)
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

        entry.title = form.title.data.title()
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
            try:
                new_tag = models.Tag.get(models.Tag.name == tag.title())
            except models.DoesNotExist:
                new_tag = models.Tag.create(name=tag.title())

            models.TagList.create(tag=new_tag, entry=entry)

        return redirect(url_for('view_entry', slug=entry.title))

    return render_template('edit.html', form=form, title=title, tags=tags)


@app.route('/entries/delete/<slug>', methods=('GET', 'POST'))
def del_entry(slug):
    entry = models.Entry.get(models.Entry.title == slug)

    try:
        tag_lists = models.TagList.get(entry=entry)
        if len(tag_lists) > 1:
            for ls in tag_lists:
                ls.delete_instance()
        else:
            tag_lists[0].delete_instance()
    except models.DoesNotExist:
        pass

    entry.delete_instance()

    return redirect(url_for('index'))


@app.route('/tags/<tag>')
def tag_list(tag):
    entries = (models.Entry
               .select()
               .join(models.TagList)
               .join(models.Tag)
               .where(models.Tag.name == tag)).order_by(-models.Entry.date_created)

    return render_template('tag_list.html', entries=entries, tag=tag)


if __name__ == '__main__':
    app.run(debug=DEBUG)
