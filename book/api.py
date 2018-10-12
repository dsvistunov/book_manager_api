from flask import (
    Blueprint, request, jsonify
)

from book.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/list', methods=('Get',))
def list_all():
    db = get_db()
    books = db.execute(
        'SELECT * FROM book'
    ).fetchall()
    return jsonify(books)


@bp.route('/create', methods=('POST',))
def create():
    if request.json:
        autor = request.json.get("autor", None)
        title = request.json.get("title", None)
        published = request.json.get("published", None)
        error = None

        if autor is None:
            error = "Autor is required"
        elif title is None:
            error = "Title is required"
        elif published is None:
            error = "Published is required"

        if error is not None:
            return jsonify(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO book (author_id, title, published)'
                ' VALUES (?, ?, ?)',
                (autor, title, published)
            )
            db.commit()
            return jsonify({'success': True})

    return jsonify({"success": False})


@bp.route('/get/<int:book_id>', methods=('GET',))
def get(book_id):
    db = get_db()
    book = db.execute(
        'SELECT * FROM book WHERE id = ?',
        (book_id,)
    ).fetchone()
    return jsonify(book)


@bp.route('/update/<int:book_id>', methods=('PUT',))
def update(book_id):
    if request.json:
        autor = request.json.get("autor", None)
        title = request.json.get("title", None)
        published = request.json.get("published", None)
        error = None

        if autor is None:
            error = "Autor is required"
        elif title is None:
            error = "Title is required"
        elif published is None:
            error = "Published is required"

        if error is not None:
            return jsonify(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE book SET author_id = ?, title = ?, published = ? WHERE id = ?',
                (autor, title, published, book_id,)
            )
            db.commit()
            return jsonify({"updated": True})
    return jsonify({"updated": False})


@bp.route('/delete/<int:book_id>', methods=('DELETE',))
def delete(book_id):
    if request.json:
        db = get_db()
        exist = db.execute(
            'SELECT * FROM book WHERE id = ?',
            (book_id,)
        ).fetchone()
        if exist:
            db.execute(
                'DELETE FROM book WHERE id = ?',
                (book_id,)
            )
            db.commit()
            return jsonify({"deleted": True})
        else:
            message = "Book with id %s doesn't exist" % book_id
            return jsonify({"error": message})


@bp.route('/filter', methods=('POST',))
def filter():
    if request.json:
        field = request.json.get("field", None)
        option = request.json.get("option", None)
        value = request.json.get("value", None)
        error = None

        if field is None:
            error = "Field is required"
        elif option is None:
            error = "Option is required"
        elif value is None:
            error = "Value is required"

        if error is not None:
            return jsonify({"error": error})
        else:
            db = get_db()

            if option == 'startswith':
                pattern = '"{}%"'.format(value)
                sql_query = 'SELECT * FROM book WHERE {} LIKE {}'.format(field, pattern)
                result = db.execute(sql_query).fetchall()
            elif option == 'endswith':
                pattern = '"%{}"'.format(value)
                sql_query = 'SELECT * FROM book WHERE {} LIKE {}'.format(field, pattern)
                result = db.execute(sql_query).fetchall()
            elif option == 'exact':
                sql_query = 'SELECT * FROM book WHERE {} = {}'.format(field, value)
                result = db.execute(sql_query).fetchall()

            return jsonify(result)
