import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from . import db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    '''view function for the register page'''
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        database = db.get_db()
        error = None

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"

        if error is None:
            try:
                database.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password))
                )
                database.commit()
            except database.IntegrityError:
                error = f"{username} is already registered"
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    '''view function for the login page'''
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        database = db.get_db()
        error = None
        user = database.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username"
        elif not check_password_hash(user['password'], password):
            error = "Incorrect password"
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    '''view function to get data from the user. It checks if the user_id is stored in the session.
    The data is then retrieved from the database using the user_id and stored on g.user'''
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = db.get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    '''removes the user_id from the session. Then load_logged_in_user won't load a user on subsequent requests'''
    session.clear()
    return redirect(url_for('index'))