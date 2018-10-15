from flask_marshmallow import Marshmallow
from book import app, Author, Book


ma = Marshmallow(app)


class AuthorSchema(ma.ModelSchema):
    class Meta:
        model = Author


class BookSchema(ma.ModelSchema):
    class Meta:
        model = Book


author_schema = AuthorSchema()
book_schema = BookSchema()
books_schema = BookSchema(many=True)
