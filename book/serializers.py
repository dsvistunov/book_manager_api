from flask_marshmallow import Marshmallow
from book.models import Author, Book


ma = Marshmallow()


class AuthorSchema(ma.ModelSchema):
    class Meta:
        model = Author


class BookSchema(ma.ModelSchema):
    class Meta:
        model = Book


author_schema = AuthorSchema()
book_schema = BookSchema()
books_schema = BookSchema(many=True)
