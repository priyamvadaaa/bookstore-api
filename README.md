# Bookstore API

A simple Flask-RESTful API to manage books in a bookstore. Data is stored persistently in a local book.json file (no external database required).

## Endpoints

- **GET /books**: List all books
  - Optional query: `?title=<search_term>` to search books by title (case-insensitive substring match)
- **POST /books**: Add a new book
  - Request JSON: `{ "title": str, "author": str, "price": float, "stock": int }`
- **GET /books/<id>**: Get details of a specific book
- **PUT /books/<id>**: Update a book
  - Request JSON: Any subset of `{ "title", "author", "price", "stock" }`
- **DELETE /books/<id>**: Delete a book
- **GET /books/title/<title>**: Search for books by title (case-insensitive substring match)
- **GET /books/sorted-by-price**: List all books sorted in ascending order of price

## Data Persistence
- All book records are stored in `book.json` in the project directory.
- Any changes (add, update, delete) are saved immediately and persist across server restarts.

## Error Handling
- 400 Bad Request: Missing or invalid fields, negative stock, wrong data types
- 404 Not Found: Book does not exist, or search yields no results

## Example Usage
```bash
# List all books
curl -X GET http://localhost:5000/books

# Add a new book
curl -X POST http://localhost:5000/books -H "Content-Type: application/json" -d '{"title":"Dune","author":"Frank Herbert","price":12.99,"stock":5}'

# Get details of a specific book
curl -X GET http://localhost:5000/books/1

# Update a book
curl -X PUT http://localhost:5000/books/1 -H "Content-Type: application/json" -d '{"stock":10}'

# Delete a book
curl -X DELETE http://localhost:5000/books/1

# Search books by title (query param)
curl -X GET "http://localhost:5000/books?title=Brave"

# Search books by title (path param)
curl -X GET http://localhost:5000/books/title/Brave

# List all books sorted by price
curl -X GET http://localhost:5000/books/sorted-by-price
```

## Running the API
```bash
python main.py
```

## Testing
```bash
pytest
```

## Logging
Structured logs are output to the console for all API actions.
