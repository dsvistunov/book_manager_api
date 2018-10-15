import os
import click
from flask import Flask
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
path_to = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'books.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + path_to
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@click.command('init-db')
@with_appcontext
def init_db_command():
    db.create_all()
    click.echo('Db init')


app.cli.add_command(init_db_command)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(120),  nullable=False)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    author = db.relationship('Author', backref=db.backref('books', lazy=True))
    title = db.Column(db.String(120), nullable=False)
    published = db.Column(db.Date, nullable=False)

from . import api
app.register_blueprint(api.bp)
