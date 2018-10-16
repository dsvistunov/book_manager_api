import os
import pytest
from book import create_app
from book.models import db, Author, Book
from datetime import datetime


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""

    path_to = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test.db')
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + path_to,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })

    # create the database and load test data
    with app.app_context():
        db.create_all()

        author1 = Author(first_name='First', last_name='Author')
        author2 = Author(first_name='Second', last_name='Author')
        db.session.add(author1)
        db.session.add(author2)
        Book(author=author1, title='Test book', published=datetime(2000, 1, 1))
        Book(author=author2, title='Test book', published=datetime(2000, 1, 1))

        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()

    return app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()
