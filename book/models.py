import click
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext


db = SQLAlchemy()


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

    def save(self):
        if self.id is None:
            db.session.add(self)
            db.session.commit()
        return self


@click.command('init-db')
@with_appcontext
def init_db_command():
    db.create_all()
    click.echo('Db init')
