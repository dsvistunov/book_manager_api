from datetime import datetime
from flask import (
    Blueprint, request, jsonify
)

from book.models import Author, Book, db
from .serializers import book_schema, books_schema

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/books', methods=('Get',))
def list_all():
    books = Book.query
    if request.args:
        for key in request.args:
            if hasattr(Book, key):
                books = books.join(getattr(Book, key), aliased=True)\
                    .filter_by(first_name=request.args[key])
            elif '__' in key:
                field, option = key.split('__')
                if option == 'startswith':
                    books = books.filter(getattr(Book, field)
                                         .startswith(request.args[key]))
                elif option == 'endswith':
                    books = books.filter(getattr(Book, field)
                                         .endswith(request.args[key]))

    serializer = books_schema.dump(books.all())
    return jsonify(serializer.data)


@bp.route('/books', methods=('POST',))
def create():
    if request.json:
        author_id = request.json.get("author", 0)
        author = Author.query.get(author_id)
        title = request.json.get("title", None)
        date_str = request.json.get("published", None)
        error = None

        if author is None:
            error = "Autor is required"
        elif title is None:
            error = "Title is required"
        elif date_str is None:
            error = "Published is required"
        else:
            published = datetime.strptime(date_str, '%Y-%m-%d')

        if error is not None:
            return jsonify({'error': error})
        else:
            book = Book(author=author, title=title, published=published)
            db.session.add(book)
            db.session.commit()
            return jsonify({'success': True})

    return jsonify({"success": False})


@bp.route('/books/<int:book_id>', methods=('GET',))
def get(book_id):
    book = Book.query.get_or_404(book_id)
    serializer = book_schema.dump(book)
    return jsonify(serializer.data)


@bp.route('/books/<int:book_id>', methods=('PUT',))
def update(book_id):
    if request.json:
        author_id = request.json.get("author", None)
        author = Author.query.get_or_404(author_id)
        title = request.json.get("title", None)
        date_str = request.json.get("published", None)
        published = datetime.strptime(date_str, '%Y-%m-%d')
        error = None

        if author is None:
            error = "Autor is required"
        elif title is None:
            error = "Title is required"
        elif published is None:
            error = "Published is required"

        if error is not None:
            return jsonify(error)
        else:
            book = Book.query.get_or_404(book_id)
            book.author = author
            book.title = title
            book.published = published
            db.session.commit()
            return jsonify({"updated": True})
    return jsonify({"updated": False})


@bp.route('/books/<int:book_id>', methods=('DELETE',))
def delete(book_id):
    if request.json:
        book = Book.query.get_or_404(book_id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return jsonify({"deleted": True})
        else:
            message = "Book with id %s doesn't exist" % book_id
            return jsonify({"error": message})
    return jsonify({"deleted": False})
