import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    '''this function is used to check if a connection exists already. If one does not exist, the function creates
    a connection and returns it. It is like a getter.'''
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    '''checks dictionary for 'db' key, if it does exist it will close the connection'''
    db = g.pop('db', None)

    if db is not None:
        db.close()
