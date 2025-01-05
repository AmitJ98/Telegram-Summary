import psycopg2
from psycopg2 import sql
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()


DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")



#need to change it to global time timestamp and add typing of timestamp
def connect_to_db():
    """Connect to the database and return the connection object."""
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print(f"[SUCCESS] Connected to the database '{DB_NAME}' successfully on host '{DB_HOST}:{DB_PORT}'.")
        return connection
    
    except Exception as e:
        print(f"[ERROR] Failed to connect to the database. Reason: {e}")
        return None


def insert_new_user(id: int, api_key: str, api_hash: str, chats_to_summarize: list[str], time_to_summarize=None):
    """Insert a new user into the database, into the users table.
       Return True if the user was inserted successfully, False otherwise."""
    
    connection_to_database = connect_to_db()
    if connection_to_database is None:
        return False

    query = """
    INSERT INTO users_data (id, api_key, api_hash, chats, time)
    VALUES (%s, %s, %s, %s, %s);
    """
    try:
        cursor = connection_to_database.cursor()
        cursor.execute(query, (id, api_key, api_hash, chats_to_summarize, time_to_summarize))
        connection_to_database.commit()
        print(f"[SUCCESS] New user inserted successfully! Details:\n"
              f"  ID: {id}\n"
              f"  API Key: {api_key}\n"
              f"  API Hash: {api_hash}\n"
              f"  Chats: {chats_to_summarize}\n"
              f"  Timestamp: {time_to_summarize if time_to_summarize else 'Default (NOW())'}")
        return True
    
    except Exception as e:
        print(f"[ERROR] Failed to insert user ID {id}. Reason: {e}")
        connection_to_database.rollback()
        return False


def fetch_user_data(id: int):
    """Fetch a user from the database, from the users table.
       Return the user if the user was fetched successfully, None otherwise."""

    connection_to_database = connect_to_db()
    if connection_to_database is None:
        return None
    
    query = """
    SELECT *
    FROM users_data
    WHERE id = %s;
    """
    try:
        cursor = connection_to_database.cursor()
        cursor.execute(query, (id,))
        user = cursor.fetchone()
        if user:
            print(f"[SUCCESS] User fetched successfully! ID: {user[0]}\n")
            return user
        
        else:
            print(f"[INFO] No user found with ID: {id}.")
            return None
        
    except Exception as e:
        print(f"[ERROR] Failed to fetch user with ID {id}. Reason: {e}")
        return None


def delete_user(id: int):
    """Delete a user from the database, from the users table.
       Return True if the user was deleted successfully or if the user is not found, False otherwise."""
    
    connection_to_database = connect_to_db()
    if connection_to_database is None:
        return False
    
    query = """
    DELETE FROM users_data
    WHERE id = %s;
    """
    try:
        cursor = connection_to_database.cursor()
        cursor.execute(query, (id,))
        if cursor.rowcount == 0:  # No rows found
            print(f"[INFO] User ID {id} does not exist. No action taken.")
        else:
            print(f"[SUCCESS] User ID {id} deleted successfully.")
        connection_to_database.commit()
        return True
    
    except Exception as e:
        print(f"[ERROR] Failed to delete user ID {id}. Reason: {e}")
        connection_to_database.rollback()
        return False


def update_chat_list(id: int, new_chats: list[str]):
    """Update the chat list of a user in the database, in the users table.
       Return True if the chat list was updated successfully or if the user is not found, False otherwise."""
    
    connection_to_database = connect_to_db()
    if connection_to_database is None:
        return False

    query = """
    UPDATE users_data
    SET chats = %s
    WHERE id = %s;
    """
    try:
        cursor = connection_to_database.cursor()
        cursor.execute(query, (new_chats, id))
        if cursor.rowcount == 0:  # No rows found
            print(f"[INFO] User ID {id} does not exist. Chat list update skipped.")
        else:
            print(f"[SUCCESS] Chat list for user ID {id} updated successfully to: {new_chats}")
        connection_to_database.commit()
        return True
    
    except Exception as e:
        print(f"[ERROR] Failed to update chat list for user ID {id}. Reason: {e}")
        connection_to_database.rollback()
        return False


def update_time(id: int, new_time):
    """Update the time of a user in the database, in the users table.
       Return True if the time was updated successfully or if the user is not found, False otherwise."""
    
    connection_to_database = connect_to_db()
    if connection_to_database is None:
        return False

    query = """
    UPDATE users_data
    SET time = %s
    WHERE id = %s;
    """
    try:
        cursor = connection_to_database.cursor()
        cursor.execute(query, (new_time, id))
        if cursor.rowcount == 0:  # No rows found
            print(f"[INFO] User ID {id} does not exist. Time update skipped.")
        else:
            print(f"[SUCCESS] Time for user ID {id} updated successfully to: {new_time}")
        connection_to_database.commit()
        return True
    
    except Exception as e:
        print(f"[ERROR] Failed to update time for user ID {id}. Reason: {e}")
        connection_to_database.rollback()
        return False
    


