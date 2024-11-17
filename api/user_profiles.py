# Module for Managing User Profiles

from flask import Blueprint, jsonify, request

from db import get_db_connection

user_profiles_routes = Blueprint('user_profiles', __name__)


@user_profiles_routes.app_errorhandler(404)
def page_not_found(e):
    return jsonify({
        "error_code": 404,
        "message": "The resource could not be found."
    }), 404


@user_profiles_routes.app_errorhandler(500)
def internal_server_error(e):
    return jsonify({
        "error_code": 500,
        "message": "An internal error occured"
    }), 500


@user_profiles_routes.app_errorhandler(405)
def method_not_allowed(e):
    return jsonify({
        "error_code": "405",
        "message": "The method is not allowed for the requested URL"
    }), 405



@user_profiles_routes.route('', methods=['POST'])
def create_profile():
    data = request.get_json()

    username = data['username'],
    email =     data['email'],
    reading_preferences =    data['reading_preferences'],
    favorite_genres =    data['favorite_genres'],
    books_owned =    data['books_owned'],
    books_wish_to_acquire =    data['books_wish_to_acquire']
   

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO profiles (username, email, reading_preferences, favorite_genres, books_owned, books_wish_to_acquire) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        (username, email, reading_preferences, ",".join(favorite_genres), ",".join(books_owned), ",".join(books_wish_to_acquire))
    )
    connection.commit()
    cursor.close()


    return jsonify({"message": "Profile created successfully"}), 201

@user_profiles_routes.route('/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM profiles WHERE id = %s", (user_id,))
    profile = cursor.fetchone()
    cursor.close()

    if profile:
        return jsonify(profile)
    return jsonify({"error": "Profile not found"}), 404

@user_profiles_routes.route('/<int:user_id>', methods=['PUT'])
def update_profile(user_id):
    data = request.get_json()
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE profiles SET username = %s, email = %s, reading_preferences = %s, "
        "favorite_genres = %s, books_owned = %s, books_wish_to_acquire = %s WHERE id = %s",
        (
            data['username'], data['email'], data['reading_preferences'], 
            ",".join(data['favorite_genres']), ",".join(data['books_owned']), 
            ",".join(data['books_wish_to_acquire']), user_id
        )
    )
    connection.commit()
    cursor.close()
    return jsonify({"message": "Profile updated successfully"})

@user_profiles_routes.route('/<int:user_id>', methods=['DELETE'])
def delete_profile(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM profiles WHERE id = %s", (user_id,))
    connection.commit()
    cursor.close()
    return jsonify({"message": "Profile deleted successfully"})