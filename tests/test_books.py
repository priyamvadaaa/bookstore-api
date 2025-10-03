import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from main import app
import time

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_list_books(client):
    resp = client.get('/books')
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert all('title' in b and 'author' in b and 'price' in b and 'stock' in b for b in data)

def test_add_book(client):
    new_book = {'title': 'Dune', 'author': 'Frank Herbert', 'price': 12.99, 'stock': 5}
    resp = client.post('/books', json=new_book)
    assert resp.status_code == 201
    data = resp.get_json()
    for k in new_book:
        assert data[k] == new_book[k]
    assert 'id' in data

def test_get_book(client):
    resp = client.get('/books/1')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['id'] == 1
    assert 'title' in data

def test_update_book(client):
    update = {'stock': 99}
    resp = client.put('/books/1', json=update)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['stock'] == 99

def test_delete_book(client):
    resp = client.delete('/books/2')
    assert resp.status_code == 204
    # Should now 404
    resp2 = client.get('/books/2')
    assert resp2.status_code == 404

def test_performance_list_books(client):
    start = time.time()
    resp = client.get('/books')
    duration = time.time() - start
    assert resp.status_code == 200
    assert duration < 0.2, f"GET /books took {duration:.3f}s, exceeds 200ms"

def test_search_books_found(client):
    resp = client.get('/books?title=1984')
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert any('1984' in b['title'] for b in data)

def test_search_books_not_found(client):
    resp = client.get('/books?title=Nonexistent')
    assert resp.status_code == 404
    data = resp.get_json()
    assert 'message' in data
    assert 'No books found' in data['message']

def test_sorted_books_by_price(client):
    # Add a few books with different prices
    client.post('/books', json={'title': 'Cheap Book', 'author': 'A', 'price': 1.99, 'stock': 2})
    client.post('/books', json={'title': 'Expensive Book', 'author': 'B', 'price': 99.99, 'stock': 1})
    client.post('/books', json={'title': 'Mid Book', 'author': 'C', 'price': 10.00, 'stock': 5})
    resp = client.get('/books/sorted-by-price')
    assert resp.status_code == 200
    data = resp.get_json()
    prices = [b['price'] for b in data]
    assert prices == sorted(prices)
    # Check that all books are present
    titles = [b['title'] for b in data]
    assert 'Cheap Book' in titles and 'Mid Book' in titles and 'Expensive Book' in titles

def test_sorted_books_by_price_empty(client):
    # Remove all books
    global books
    books.clear()
    resp = client.get('/books/sorted-by-price')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data == []

def test_search_books_by_author(client):
    # Add test books
    books = [
        {'id': 1, 'title': 'Book A', 'author': 'Author X', 'price': 10.0, 'stock': 5},
        {'id': 2, 'title': 'Book B', 'author': 'Author Y', 'price': 12.0, 'stock': 3},
        {'id': 3, 'title': 'Book C', 'author': 'Author X', 'price': 8.0, 'stock': 7},
    ]
    with open('book.json', 'w') as f:
        import json; json.dump(books, f)
    # Search for Author X
    response = client.get('/books/author/Author X')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert all('Author X' in b['author'] for b in data)
    # Search for non-existent author
    response = client.get('/books/author/Unknown')
    assert response.status_code == 404
    assert 'book not found' in response.get_json()['message'].lower()

def test_search_books_by_author_edge_cases(client):
    # Add books with special characters and similar author names
    books = [
        {'id': 1, 'title': 'Book D', 'author': 'Author-X', 'price': 10.0, 'stock': 5},
        {'id': 2, 'title': 'Book E', 'author': 'Author X', 'price': 12.0, 'stock': 3},
        {'id': 3, 'title': 'Book F', 'author': 'author x', 'price': 8.0, 'stock': 7},
        {'id': 4, 'title': 'Book G', 'author': 'Author X.', 'price': 9.0, 'stock': 2},
    ]
    with open('book.json', 'w') as f:
        import json; json.dump(books, f)
    # Search for 'Author X' (case-insensitive, partial)
    response = client.get('/books/author/author x')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) >= 3  # Should match Author X, author x, Author X.
    # Search for special character
    response = client.get('/books/author/Author-X')
    assert response.status_code == 200
    data = response.get_json()
    assert any('Author-X' in b['author'] for b in data)
    # Search for whitespace
    response = client.get('/books/author/ ')
    assert response.status_code == 400
