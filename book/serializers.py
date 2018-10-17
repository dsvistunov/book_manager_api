from flask_marshmallow import Marshmallow
from book.models import Author, Book, db
from marshmallow import validates_schema, ValidationError

ma = Marshmallow()


class AuthorSchema(ma.ModelSchema):
    class Meta:
        model = Author
        sqla_session = db.session


class BookSchema(ma.ModelSchema):
    class Meta:
        model = Book
        sqla_session = db.session

    @validates_schema
    def validate_fields_requered(self, data):
        author_id = data.get('author', None)
        title = data.get('title', None)
        date = data.get('published', None)

        if author_id is None:
            raise ValidationError('Author is required')
        elif title is None:
            raise ValidationError('Title is required')
        elif date is None:
            raise ValidationError('Published is required')

    def save(self):
        pass


author_schema = AuthorSchema()
book_schema = BookSchema()
books_schema = BookSchema(many=True)
