import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy  # , or_
from flask_cors import CORS
import random

from models import setup_db, Book

BOOKS_PER_SHELF = 8

# @TODO: General Instructions
#   - As you're creating endpoints, define them and then search for 'TODO' within the frontend to update the endpoints there.
#     If you do not update the endpoints, the lab will not work - of no fault of your API code!
#   - Make sure for each route that you're thinking through when to abort and with which kind of error
#   - If you change any of the response body keys, make sure you update the frontend to correspond.


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    # @TODO: Write a route that retrivies all books, paginated.
    #         You can use the constant above to paginate by eight books.
    #         If you decide to change the number of books per page,
    #         update the frontend to handle additional books in the styling and pagination
    #         Response body keys: 'success', 'books' and 'total_books'
    # TEST: When completed, the webpage will display books including title, author, and rating shown as stars
    @app.route('/books', methods=['GET', 'POST'])
    def get_books():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * BOOKS_PER_SHELF
        end = start + BOOKS_PER_SHELF
        books = Book.query.order_by(Book.id).all()
        formatted_books = [book.format() for book in books]
        limit = page * 8

        if len(formatted_books) < (limit):
        # if len(formatted_books) not in range((limit - 7), limit):
            abort(404)
        
        return jsonify({
                'success': True,
                'books': formatted_books[start:end],
                'total_books': len(formatted_books)
            })
        
    # @TODO: Write a route that will update a single book's rating.
    #         It should only be able to update the rating, not the entire representation
    #         and should follow API design principles regarding method and route.
    #         Response body keys: 'success'
    # TEST: When completed, you will be able to click on stars to update a book's rating and it will persist after refresh
    @app.route('/books/<int:book_id>', methods=['PATCH'])
    def update_book(book_id):

        object = request.get_json()

        try:
            book = Book.query.filter(Book.id==book_id).one_or_none()
            if book is None:
                abort(404)
            
            if 'rating' in object:
                book.rating = int(object.get('rating'))

            book.update()

            return jsonify({
                'success': True,
                'id': book.id,
                'rating': book.rating
            })

        except:
            abort(404)
        pass

    # @TODO: Write a route that will delete a single book.
    #        Response body keys: 'success', 'deleted'(id of deleted book), 'books' and 'total_books'
    #        Response body keys: 'success', 'books' and 'total_books'
    @app.route('/books/<int:book_id>', methods=['DELETE'])
    def delete_books(book_id):
        
        try:
            page = request.args.get('page', 1, type=int)
            start = (page - 1) * BOOKS_PER_SHELF
            end = start + BOOKS_PER_SHELF
            book = Book.query.filter(Book.id==book_id).one_or_none()
            if book is None:
                abort(404)

            book.delete()

            current_books = Book.query.order_by(Book.id).all()
            formatted_books = [cur_book.format() for cur_book in current_books]
            limit = page * 8

            if len(formatted_books) < (limit):
            # if len(formatted_books) not in range((limit - 7), limit):
                abort(404)

            return jsonify({
                "success": True,
                "deleted": book_id,
                "books": formatted_books[start:end],
                "total_books": len(formatted_books)
            })
        except:
            abort(422)

    # TEST: When completed, you will be able to delete a single book by clicking on the trashcan.

    # @TODO: Write a route that create a new book.
    #        Response body keys: 'success', 'created'(id of created book), 'books' and 'total_books'
    # TEST: When completed, you will be able to a new book using the form. Try doing so from the last page of books.
    #       Your new book should show up immediately after you submit it at the end of the page.
    @app.route('/books', methods=['POST'])
    def create_book():
        object = request.get_json()

        new_title = object.get('title', None)
        new_author = object.get('author', None)
        new_rating = object.get('rating', None)

        try:
            book = Book(title=new_title, author=new_author, rating=new_rating)
            book.insert()

            current_books = Book.query.order_by(Book.id).all()
            formatted_books = [cur_book.format() for cur_book in current_books]
            limit = page * 8

            if len(formatted_books) < (limit):
            # if len(formatted_books) not in range((limit - 7), limit):
                abort(404)

            return jsonify({
                "success": True,
                "created": book.id,
                "books": formatted_books[start:end],
                "total": len(formatted_books)
            })
        except:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Reource not found in our DB"
        }), 404

    @app.errorhandler(422)
    def unprocessable():
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unable to process your request"
        }), 422

    @app.errorhandler(400)
    def bad_request():
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def wrong_method(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        }), 405

        
    return app
