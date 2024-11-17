# Module for Login/Signup for users


from flask import request, jsonify, Blueprint
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from db import get_db_connection
from datetime import timedelta
import mysql.connector




bcrypt = Bcrypt()


user_manager_routes = Blueprint('user_manager', __name__)


@user_manager_routes.app_errorhandler(404)
def page_not_found(e):
    return jsonify({
        "error_code": 404,
        "message": "The resource could not be found."
    }), 404


@user_manager_routes.app_errorhandler(500)
def internal_server_error(e):
    return jsonify({
        "error_code": 500,
        "message": "An internal error occured"
    }), 500


@user_manager_routes.app_errorhandler(405)
def method_not_allowed(e):
    return jsonify({
        "error_code": "405",
        "message": "The method is not allowed for the requested URL"
    }), 405



# User Signup

@user_manager_routes.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Hash the password
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert user details into the database
        cursor.execute("INSERT INTO Users (username, email, password_hash) VALUES (%s, %s, %s)", 
                       (username, email, password_hash))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'User registered successfully'}), 201

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

# User Login
@user_manager_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch user by email
    cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and bcrypt.check_password_hash(user['password_hash'], password):
        # Create JWT access token
        access_token = create_access_token(identity=user['user_id'])
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

# Update Password
@user_manager_routes.route('/update-password', methods=['PUT'])
@jwt_required()
def update_password():
    data = request.get_json()
    new_password = data.get('new_password')

    # Get user ID from JWT token
    user_id = get_jwt_identity()

    # Hash the new password
    new_password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Update password in the database
        cursor.execute("UPDATE Users SET password_hash = %s WHERE user_id = %s", 
                       (new_password_hash, user_id))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Password updated successfully'}), 200

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

# Get User Profile
@user_manager_routes.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch user profile details
    cursor.execute("SELECT user_id, username, email, created_at FROM Users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        return jsonify({'user': user}), 200
    else:
        return jsonify({'error': 'User not found'}), 404