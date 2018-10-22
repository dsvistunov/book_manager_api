from datetime import datetime
from flask import (
    Blueprint, request, jsonify
)

from book.models import Author, Book, db
from .schema import book_schema, books_schema

bp = Blueprint('api', __name__, url_prefix='/api')


def _filter(instanse, args):
    query = instanse.query
    for key in args:
        if hasattr(instanse, key):
            if key == 'author':
                query = query.join(getattr(instanse, key), aliased=True) \
                    .filter_by(first_name=request.args[key])
            else:
                query = query.filter(getattr(instanse, key) == args[key])
        elif '__' in key:
            field, option = key.split('__')
            if option == 'startswith':
                query = query.filter(getattr(instanse, field)
                                     .startswith(args[key]))
            elif option == 'endswith':
                query = query.filter(getattr(instanse, field)
                                     .endswith(args[key]))
    return query


@bp.route('/books', methods=('Get',))
def list_all():
    if request.is_json:
        if request.args:
            books = _filter(Book, request.args)
        else:
            books = Book.query
        serializer = books_schema.dump(books.all())
        return jsonify(serializer.data)
    else:
        return jsonify({"error": "request is %s, must be application/json" % request.content_type})


@bp.route('/books', methods=('POST',))
def create():
    if request.is_json:
        book = book_schema.load(request.json)
        if book.errors:
            return jsonify(book.errors), 400
        else:
            book = book.data.save()
            serialized = book_schema.dump(book)
            return jsonify(serialized.data)
    else:
        return jsonify({"error": "request is %s, must be application/json" % request.content_type})


@bp.route('/books/<int:book_id>', methods=('GET',))
def get(book_id):
    if request.is_json:
        book = Book.query.get_or_404(book_id)
        serializer = book_schema.dump(book)
        return jsonify(serializer.data)
    else:
        return jsonify({"error": "request is %s, must be application/json" % request.content_type})


@bp.route('/books/<int:book_id>', methods=('PUT',))
def update(book_id):
    if request.is_json:
        exit_book = Book.query.get(book_id)
        if exit_book:
            book = book_schema.load(request.json, instance=exit_book)
            if book.errors:
                return jsonify(book.errors), 400
            else:
                book = book.data.save()
                serialized = book_schema.dump(book)
                return jsonify(serialized.data)
        else:
            return jsonify({"error": "Book with id %s doesn't exist" % book_id})
    else:
        return jsonify({"error": "request is %s, must be application/json" % request.content_type})


@bp.route('/books/<int:book_id>', methods=('DELETE',))
def delete(book_id):
    if request.is_json:
        book = Book.query.get_or_404(book_id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return jsonify({"deleted": True})
        else:
            message = "Book with id %s doesn't exist" % book_id
            return jsonify({"error": message})
    else:
        return jsonify({"error": "request is %s, must be application/json" % request.content_type})
