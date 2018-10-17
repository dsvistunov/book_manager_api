import os
from flask import Flask


def create_app(config=None):
    app = Flask(__name__)
    path_to = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'books.db')
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + path_to,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(config)

    from book.models import db, init_db_command
    db.init_app(app)
    app.cli.add_command(init_db_command)

    from book.schema import ma
    ma.init_app(app)

    from . import api
    app.register_blueprint(api.bp)

    return app









