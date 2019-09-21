from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.database import DatabaseConnection

bp = Blueprint('blog', __name__)


def get_post(id, check_author=True):
    post = DatabaseConnection().findOne('properties', id)

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/')
def index():
    db = DatabaseConnection()
    posts = db.findAll("properties")
    return render_template('index.html', posts=posts)



@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        address = request.form['address']
        price = request.form['price']
        description = request.form['description']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = DatabaseConnection()
            db.insert("properties", {"address": address,
                                     "price": price,
                                     "owner": g.user['id'],
                                     "description": description})
            return redirect(url_for('index'))

    return render_template('properties/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = DatabaseConnection
            db.update(properties, title, body)
            return redirect(url_for('index'))

    return render_template('properties/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    db = DatabaseConnection()
    db.properties
    return redirect(url_for('properties.index'))
