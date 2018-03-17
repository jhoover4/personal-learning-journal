from flask import Flask, g, render_template

import models

DEBUG = False

app = Flask(__name__)


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
def index():
    return render_template('index.html')


@app.route('/entries')
def list_entries():
    return render_template('index.html')


@app.route('/entries/<slug>')
def view_entry(slug):
    return render_template('detail.html')


@app.route('/entries/edit/slug', methods=('GET', 'POST'))
def edit_entry(slug):
    return render_template('edit.html')


@app.route('/entries/delete/slug', methods=('GET', 'POST'))
def del_entry(slug):
    return render_template('edit.html')


@app.route('/entry', methods=('GET', 'POST'))
def add_entry():
    return render_template('new.html')


if __name__ == '__main__':
    app.run(debug=DEBUG)
