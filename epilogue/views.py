from __future__ import absolute_import

from app import app
from flask import render_template
from werkzeug.exceptions import NotFound

from models import Document


@app.route('/')
def index():
    posts = Document.select()
    return render_template("index.html", **{
        "posts": posts,
    })


@app.route('/essay/<string:slug>/')
def post(slug):
    try:
        doc = Document.get(slug=slug)
    except Document.DoesNotExist:
        raise NotFound()

    return render_template("document.html", **{
        "document": doc,
    })


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404