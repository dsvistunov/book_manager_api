from flask_marshmallow import Marshmallow
from book.models import Author, Book, db
from marshmallow import fields


ma = Marshmallow()


class AuthorSchema(ma.ModelSchema):
    class Meta:
        model = Author
        sqla_session = db.session


class BookSchema(ma.ModelSchema):
    class Meta:
        model = Book
        sqla_session = db.session

    author_id = fields.Integer(required=True)
    title = fields.String(required=True)
    published = fields.Date(required=True)


author_schema = AuthorSchema()
book_schema = BookSchema()
books_schema = BookSchema(many=True)
