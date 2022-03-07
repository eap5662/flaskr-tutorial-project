import os
from flask import Flask


def create_app(test_config=None):
    '''this function is the application factory. It is used to configure and return the app'''
    app = Flask(__name__, instance_path=r'C:\Users\ihelp\flaskr-tutorial-project',
                instance_relative_config=True)  # app is the instance of Flask class
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
        # file path for database. 'DATABASE' is a key which will be pointed to
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

        # ensure the instance folder exists
        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass

    @app.route('/hello')
    def hello():
        return "Hello, World!"

    from . import db
    db.init_app(app)

    return app
