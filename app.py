from flask import Flask, g, render_template

import models

DEBUG = False

app = Flask(__name__)


@app.before_request
def before_request():
    """Connecting to peewee db"""
    g.db = models.DATABASE
    try:
        g.db.connect()
    except:
        pass


@app.after_request
def after_request(response):
    """Disconnecting from peewee db"""
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
    return render_template('index.html')


@app.route('/entries/edit/slug')
def edit_entry(slug):
    return render_template('index.html')


@app.route('/entries/delete/slug')
def del_entry(slug):
    return render_template('index.html')


@app.route('/entry')
def add_entry():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=DEBUG)
