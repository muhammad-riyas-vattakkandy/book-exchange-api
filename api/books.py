# Module for adding, Listing and Searching Books

from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
import mysql.connector
from datetime import timedelta
from db import get_db_connection



books_routes = Blueprint('books', __name__)


# Add a Book
@books_routes.route('', methods=['POST'])
@jwt_required()
def add_book():
    user_id = get_jwt_identity()
    data = request.get_json()

    title = data.get('title')
    author = data.get('author')
    genre = data.get('genre')
    condition = data.get('condition')  # 'New', 'Good', 'Used'
    availability = data.get('availability')  # 'Lend', 'Exchange', 'Not Available'
    location = data.get('location') 

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert book details into the database
        cursor.execute("""
            INSERT INTO Books (user_id, title, author, genre, item_condition, availability, location)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (user_id, title, author, genre, condition, availability, location))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Book added successfully'}), 201

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

# Update Book Details
@books_routes.route('/<int:book_id>', methods=['PUT'])
@jwt_required()
def update_book(book_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    title = data.get('title')
    author = data.get('author')
    genre = data.get('genre')
    condition = data.get('condition')
    availability = data.get('availability')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Update book details in the database
        cursor.execute("""
            UPDATE Books
            SET title = %s, author = %s, genre = %s, condition = %s, availability = %s
            WHERE book_id = %s AND user_id = %s
        """, (title, author, genre, condition, availability, purpose, book_id, user_id))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Book details updated successfully'}), 200

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

# View Books by User
@books_routes.route('', methods=['GET'])
@jwt_required()
def view_books():
    user_id = get_jwt_identity()

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch books for the authenticated user
        cursor.execute("SELECT * FROM Books WHERE user_id = %s", (user_id,))
        books = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify({'books': books}), 200

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

# Delete a Book
@books_routes.route('/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    user_id = get_jwt_identity()

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Delete book from the database
        cursor.execute("DELETE FROM Books WHERE book_id = %s AND user_id = %s", (book_id, user_id))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Book deleted successfully'}), 200

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500


@books_routes.route('/search-books', methods=['GET'])
@jwt_required()
def search_books():
    search_type = request.args.get('searchtype') 
    search_value = request.args.get('searchvalue') 
    print(search_type)
    
    if not search_value:
        return jsonify({'message': 'Search query is missing.'}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = f"""
    SELECT books.*, users.username 
    FROM books 
    JOIN users ON books.user_id = users.user_id 
    WHERE {search_type} LIKE \"%{search_value}%\"
"""


        print(query)

        cursor.execute(query)
        books = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify({'books': books}), 200

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    
