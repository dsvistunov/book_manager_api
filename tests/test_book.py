import json
from book.models import Book


def post_json(client, url, json_dict):
    """Send dictionary json_dict as a json to the specified url """
    return client.post(url, data=json.dumps(json_dict), content_type='application/json')


def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode('utf8'))


def test_list_all(app, client):
    books = Book.query.all()
    response = client.get('/api/books')

    assert response.status_code == 200
    assert len(json_of_response(response)) == len(books)


def test_filter_field_and_field__startswith(app, client):
    book = Book.query\
        .join(Book.author, aliased=True)\
        .filter_by(first_name='First')\
        .filter(Book.title.startswith('T'))\
        .all()
    response = client.get('/api/books?author=First&title__startswith=T')
    response = json_of_response(response)
    assert response[0]['author'] == book[0].author_id
    assert response[0]['title'] == book[0].title
    assert response[0]['published'] == str(book[0].published)


def test_filter_field_and_field__endswith(app, client):
    book = Book.query \
        .join(Book.author, aliased=True) \
        .filter_by(first_name='Second') \
        .filter(Book.title.endswith('k')) \
        .all()
    response = client.get('/api/books?author=Second&title__endswith=k')
    response = json_of_response(response)
    assert response[0]['author'] == book[0].author_id
    assert response[0]['title'] == book[0].title
    assert response[0]['published'] == str(book[0].published)


def test_create_success(app, client):
    data = {"author": 1, "title": "New test book", "published": "2000-01-01"}
    response = post_json(client, '/api/books', data)
    assert json_of_response(response) == {"success": True}


def test_create_no_author(app, client):
    data = {"title": "Some title", "published": "2000-01-01 00:00:00"}
    response = post_json(client, '/api/books', data)
    assert json_of_response(response) == {"error": "Autor is required"}


def test_create_no_title(app, client):
    data = {"author": 1, "published": "2000-01-01 00:00:00"}
    response = post_json(client, '/api/books', data)
    assert json_of_response(response) == {"error": "Title is required"}


def test_create_no_published(app, client):
    data = {"author": 1, "title": "Some title"}
    response = post_json(client, '/api/books', data)
    assert json_of_response(response) == {"error": "Published is required"}


def test_create_not_json(app, client):
    response = client.post('/api/books', data={"data": "some data"}, content_type='multipart/form-data')
    assert json_of_response(response) == {"success": False}


def test_get(app, client):
    book = Book.query.get(1)
    response = client.get('/api/books/1')
    response = json_of_response(response)
    assert response['id'] == book.id
    assert response['author'] == book.author_id
    assert response['title'] == book.title
    assert response['published'] == str(book.published)


def test_update(app, client):
    data = {"author": 1, "title": "New title", "published": "2010-10-10"}
    client.put('/api/books/1', data=json.dumps(data), content_type='application/json')
    book = Book.query.get(1)
    assert book.author_id == data['author']
    assert book.title == data['title']
    assert str(book.published) == data['published']


def test_delete(app, client):
    count = len(Book.query.all())
    response = client.delete('/api/books/1', data=json.dumps({"data": "data"}), content_type='application/json')
    assert json_of_response(response) == {"deleted": True}
    assert count - 1 == 1
