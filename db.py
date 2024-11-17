import config

import mysql.connector

from mysql.connector import Error

db_connection = None

def init_db_connection():
    """Initialize the MySQL connection with error handling."""
    global db_connection
    try:
        db_connection = mysql.connector.connect(**config.MYSQL_CONFIG)
        if db_connection.is_connected():
            print("MySQL connection successful.")
            create_profiles_table()
    except Error as e:
        raise RuntimeError(f"MySQL connection failed: {e}")

def get_db_connection():
    """Return the MySQL connection, reinitializing if necessary."""
    global db_connection
    if not db_connection or not db_connection.is_connected():
        init_db_connection()
    return db_connection



def create_profiles_table():
    """Create the user profiles table if it doesn't exist."""
    connection = get_db_connection()
    cursor = connection.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS profiles (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        reading_preferences VARCHAR(255),
        favorite_genres VARCHAR(255),
        books_owned TEXT,
        books_wish_to_acquire TEXT
    )
    """

    try:
        cursor.execute(create_table_query)
        connection.commit()
        print("Profiles table created successfully.")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()

