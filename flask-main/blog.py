from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from . import auth
from . import db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    database = db.get_db()
    posts = database.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@auth.login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = "Title is required"

        if error is not None:
            flash(error)

        else:
            database = db.get_db()
            database.execute(
                'INSERT INTO post (title, body, author)'
                ' values (?, ?, ?)',
                (title, body, g.user['id'])
            )
            database.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


