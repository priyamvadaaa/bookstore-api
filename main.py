from flask import Flask, request, jsonify
from flask_restful import Resource, Api, abort
import logging
import json

app = Flask(__name__)
api = Api(app)

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
)
logger = logging.getLogger(__name__)

BOOKS_FILE = 'book.json'

def load_books():
    try:
        with open(BOOKS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_books(books):
    with open(BOOKS_FILE, 'w') as f:
        json.dump(books, f, indent=2)

# Mocked in-memory data
books = [
    {'id': 1, 'title': '1984', 'author': 'George Orwell', 'price': 9.99, 'stock': 12},
    {'id': 2, 'title': 'Brave New World', 'author': 'Aldous Huxley', 'price': 8.99, 'stock': 7},
]

# Helper to find book by id
def get_book_or_404(book_id):
    books = load_books()
    for book in books:
        if book['id'] == book_id:
            return book
    abort(404, message=f"Book {book_id} not found")

class BookList(Resource):
    def get(self):
        books = load_books()
        search_term = request.args.get('title')
        logger.info(f'GET /books called with title search: {search_term}')
        if search_term:
            matches = [b for b in books if search_term.lower() in b['title'].lower()]
            if not matches:
                logger.info(f'No books found matching title: {search_term}')
                return {'message': f'No books found with title containing "{search_term}"'}, 404
            return matches, 200
        logger.info('GET /books called')
        return books, 200
    def post(self):
        books = load_books()
        data = request.get_json(force=True)
        logger.info(f'POST /books with data: {data}')
        if not all(k in data for k in ('title', 'author', 'price', 'stock')):
            logger.warning('POST /books missing required fields')
            abort(400, message="Missing required book fields")
        new_id = max([b['id'] for b in books], default=0) + 1
        book = {'id': new_id, **data}
        books.append(book)
        save_books(books)
        logger.info(f'Book added: {book}')
        return book, 201

class Book(Resource):
    def get(self, book_id):
        logger.info(f'GET /books/{book_id} called')
        return get_book_or_404(book_id), 200
    def put(self, book_id):
        books = load_books()
        book = next((b for b in books if b['id'] == book_id), None)
        if not book:
            abort(404, message=f"Book {book_id} not found")
        data = request.get_json(force=True)
        for k in ('title', 'author', 'price', 'stock'):
            if k in data:
                book[k] = data[k]
        save_books(books)
        logger.info(f'Book updated: {book}')
        return book, 200
    def delete(self, book_id):
        books = load_books()
        book = next((b for b in books if b['id'] == book_id), None)
        if not book:
            abort(404, message=f"Book {book_id} not found")
        books.remove(book)
        save_books(books)
        logger.info(f'Book deleted: {book}')
        return '', 204

class BookTitleSearch(Resource):
    def get(self, title):
        books = load_books()
        logger.info(f'GET /books/title/{title} called')
        matches = [b for b in books if title.lower() in b['title'].lower()]
        if not matches:
            logger.info(f'No books found matching title: {title}')
            return {'message': f'No books found with title containing "{title}"'}, 404
        return matches, 200

class BookSortedByPrice(Resource):
    def get(self):
        books = load_books()
        logger.info('GET /books/sorted-by-price called')
        sorted_books = sorted(books, key=lambda b: b['price'])
        return sorted_books, 200

class BookAuthorSearch(Resource):
    def get(self, author):
        logger.info(f'GET /books/author/{author} called')
        if not author or not author.strip():
            logger.warning('Author search term is empty or missing')
            abort(400, message="Author search term is required.")
        books = load_books()
        matches = [b for b in books if author.lower() in b['author'].lower()]
        if not matches:
            logger.info(f'No books found matching author: {author}')
            return {'message': f'No books found with author containing "{author}"'}, 404
        return matches, 200

class Home(Resource):
    def get(self):
        endpoints = {
            "List all books": "/books [GET]",
            "Add a book": "/books [POST]",
            "Get book details": "/books/<id> [GET]",
            "Update a book": "/books/<id> [PUT]",
            "Delete a book": "/books/<id> [DELETE]",
            "Search books by title (query)": "/books?title=<search_term> [GET]",
            "Search books by title (path)": "/books/title/<title> [GET]",
            "Get all books sorted by price": "/books/sort [GET]"
        }
        return {
            "Book Store API": "Welcome!",
            "available_endpoints": endpoints
        }, 200

api.add_resource(BookList, '/books')
api.add_resource(Book, '/books/<int:book_id>')
api.add_resource(BookTitleSearch, '/books/title/<string:title>')
api.add_resource(BookSortedByPrice, '/books/sort')
api.add_resource(BookAuthorSearch, '/books/author/<string:author>')
api.add_resource(Home, '/')

# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
