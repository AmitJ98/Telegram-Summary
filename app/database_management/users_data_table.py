import psycopg2
from psycopg2 import sql
from datetime import datetime
import os
from dotenv import load_dotenv
from database_management.encrypt_utils import encrypt_data, decrypt_data 

load_dotenv()


"""need check if all the functions need to be async or not"""

# TODO need to change it to global time timestamp and add typing of timestamp
def connect_to_db():
    """Connect to the database and return the connection object."""
    try:
        DB_NAME = os.getenv("DB_NAME")
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        DB_HOST = os.getenv("DB_HOST")
        DB_PORT = os.getenv("DB_PORT")
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print(f"[DATABASE SUCCESS] Connected to the database '{DB_NAME}' successfully on host '{DB_HOST}:{DB_PORT}'.")
        return connection
    
    except Exception as e:
        print(f"[DATABASE ERROR] Failed to connect to the database. Reason: {e}")
        return None


def insert_new_user(id: int, api_key: str, api_hash: str, chats_to_summarize: list[str], time_to_summarize=None):
    """Insert a new user into the database, into the users table.
       Return True if the user was inserted successfully, False otherwise."""
    
    connection_to_database = connect_to_db()
    if connection_to_database is None:
        return False
    id = str(id)
    query = """
    INSERT INTO users_data (user_id, api_id, api_hash, chats_to_summarize, time_to_summarize)
    VALUES (%s, %s, %s, %s, %s);
    """
    try:
        encrypt_api_key = encrypt_data(api_key)
        encrypt_api_hash = encrypt_data(api_hash)
        cursor = connection_to_database.cursor()
        cursor.execute(query, (id, encrypt_api_key, encrypt_api_hash, chats_to_summarize, time_to_summarize))
        connection_to_database.commit()
        print(f"[DATABASE SUCCESS] New user inserted successfully! Details:\n"
              f"  ID: {id}\n"
              f"  Chats: {chats_to_summarize}\n"
              f"  Timestamp: {time_to_summarize if time_to_summarize else 'Default (NOW())'}")
        return True
    
    except Exception as e:
        print(f"[DATABASE ERROR] Failed to insert user ID {id}. Reason: {e}")
        connection_to_database.rollback()
        return False
    
    finally:
        connection_to_database.close()


def fetch_user_data(id: int) -> dict:
    """Fetch a user from the database, decrypt api_id and api_hash, and return the user.
       Returns None if the user was not found or an error occurred."""
    
    connection_to_database = connect_to_db()
    if connection_to_database is None:
        return None

    query = """
    SELECT user_id, api_id, api_hash, chats_to_summarize, time_to_summarize
    FROM users_data
    WHERE user_id = %s;
    """
    id = str(id)
    try:
        cursor = connection_to_database.cursor()
        cursor.execute(query, (id,))
        user = cursor.fetchone()
        
        if user:

            decrypted_api_id = decrypt_data(bytes(user[1]))  
            decrypted_api_hash = decrypt_data(bytes(user[2]))  
 
            # Construct and return the decrypted user object
            decrypted_user = {
                "user_id": user[0],  
                "api_id": decrypted_api_id,  
                "api_hash": decrypted_api_hash,  
                "chats_to_summarize": user[3],  
                "time_to_summarize": user[4],  
            }
            
            print(f"[DATABASE SUCCESS] User fetched and decrypted successfully! ID: {user[0]}\n")
            return decrypted_user
        
        else:
            print(f"[DATABASE INFO] No user found with ID: {id}.")
            return None
        
    except Exception as e:
        print(f"[DATABASE ERROR] Failed to fetch user with ID {id}. Reason: {e}")
        return None
    
    finally:
        connection_to_database.close()


def delete_user(id: int):
    """Delete a user from the database, from the users table.
       Return True if the user was deleted successfully or if the user is not found, False otherwise."""
    
    connection_to_database = connect_to_db()
    if connection_to_database is None:
        return False
    
    id = str(id)
    query = """
    DELETE FROM users_data
    WHERE user_id = %s;
    """
    try:
        cursor = connection_to_database.cursor()
        cursor.execute(query, (id,))
        if cursor.rowcount == 0:  # No rows found
            print(f"[DATABASE INFO] User ID {id} does not exist. No action taken.")
        else:
            print(f"[DATABASE SUCCESS] User ID {id} deleted successfully.")
        connection_to_database.commit()
        return True
    
    except Exception as e:
        print(f"[DATABASE ERROR] Failed to delete user ID {id}. Reason: {e}")
        connection_to_database.rollback()
        return False
    
    finally:
        connection_to_database.close()


def update_chat_list(id: int, new_chats: list[str]):
    """Update the chat list of a user in the database, in the users table.
       Return True if the chat list was updated successfully or if the user is not found, False otherwise."""
    
    connection_to_database = connect_to_db()
    if connection_to_database is None:
        return False

    id = str(id)
    query = """
    UPDATE users_data
    SET chats_to_summarize = %s
    WHERE user_id = %s;
    """
    try:
        cursor = connection_to_database.cursor()
        cursor.execute(query, (new_chats, id))
        if cursor.rowcount == 0:  # No rows found
            print(f"[DATABASE INFO] User ID {id} does not exist. Chat list update skipped.")
        else:
            print(f"[DATABASE SUCCESS] Chat list for user ID {id} updated successfully to: {new_chats}")
        connection_to_database.commit()
        return True
    
    except Exception as e:
        print(f"[DATABASE ERROR] Failed to update chat list for user ID {id}. Reason: {e}")
        connection_to_database.rollback()
        return False
    
    finally:
        connection_to_database.close()


def update_time(id: int, new_time):
    """Update the time of a user in the database, in the users table.
       Return True if the time was updated successfully or if the user is not found, False otherwise."""
    
    connection_to_database = connect_to_db()
    if connection_to_database is None:
        return False

    id = str(id)
    query = """
    UPDATE users_data
    SET time_to_summarize = %s
    WHERE user_id = %s;
    """
    try:
        cursor = connection_to_database.cursor()
        cursor.execute(query, (new_time, id))
        if cursor.rowcount == 0:  # No rows found
            print(f"[DATABASE INFO] User ID {id} does not exist. Time update skipped.")
        else:
            print(f"[DATABASE SUCCESS] Time for user ID {id} updated successfully to: {new_time}")
        connection_to_database.commit()
        return True
    
    except Exception as e:
        print(f"[DATABASE ERROR] Failed to update time for user ID {id}. Reason: {e}")
        connection_to_database.rollback()
        return False
    
    finally:
        connection_to_database.close()


def check_user_existence(id: int):
    """Check if a user exists in the database.
       Return True if the user exists, False otherwise."""
    
    connection_to_database = connect_to_db()
    if connection_to_database is None:
        return False

    id = str(id)
    query = """
    SELECT user_id
    FROM users_data
    WHERE user_id = %s;
    """
    try:
        cursor = connection_to_database.cursor()
        cursor.execute(query, (id,))
        user = cursor.fetchone()
        if user:
            print(f"[DATABASE INFO] User ID {id} exists in the database.")
            return True
        else:
            print(f"[DATABASE INFO] User ID {id} does not exist in the database.")
            return False
        
    except Exception as e:
        print(f"[DATABASE ERROR] Failed to check user existence for ID {id}. Reason: {e}")
        return False
    
    finally:
        connection_to_database.close()


