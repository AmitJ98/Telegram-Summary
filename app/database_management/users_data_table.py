import psycopg2
from psycopg2 import sql
from datetime import datetime
import os
from dotenv import load_dotenv
from database_management.encrypt_utils import encrypt_data, decrypt_data 

load_dotenv()


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


def insert_new_user(user_id: int, api_key: str, api_hash: str, chats_to_summarize: list[str], time_to_summarize=None) -> bool:
    """Insert a new user into the database, into the users table.
       Return True if the user was inserted successfully, False otherwise."""
    

    user_id = str(user_id)
    query = """
    INSERT INTO users_data (user_id, api_id, api_hash, chats_to_summarize, time_to_summarize)
    VALUES (%s, %s, %s, %s, %s);
    """
    
    try:
        with connect_to_db() as connection_to_database:  
            with connection_to_database.cursor() as cursor:  
                encrypt_api_key = encrypt_data(api_key)
                encrypt_api_hash = encrypt_data(api_hash)
                cursor.execute(query, (user_id, encrypt_api_key, encrypt_api_hash, chats_to_summarize, time_to_summarize))
                connection_to_database.commit()

                print(f"[DATABASE SUCCESS] New user inserted successfully! Details:\n"
                    f"  ID: {user_id}\n"
                    f"  Chats: {chats_to_summarize}\n"
                    f"  Timestamp: {time_to_summarize if time_to_summarize else 'Default (NOW())'}")
                return True
    
    except Exception as e:
        print(f"[DATABASE ERROR] Failed to insert user ID {user_id}. Reason: {e}")
        connection_to_database.rollback()
        return False


def fetch_user_data(user_id: int) -> dict:
    """Fetch a user from the database, decrypt api_id and api_hash, and return the user.
       Returns None if the user was not found or an error occurred."""
    
    query = """
    SELECT user_id, api_id, api_hash, chats_to_summarize, time_to_summarize
    FROM users_data
    WHERE user_id = %s;
    """
    user_id = str(user_id)
    
    try:
        with connect_to_db() as connection_to_database:  
            with connection_to_database.cursor() as cursor:  
                cursor.execute(query, (user_id,))
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
                    print(f"[DATABASE INFO] No user found with ID: {user_id}.")
                    return None
        
    except Exception as e:
        print(f"[DATABASE ERROR] Failed to fetch user with ID {user_id}. Reason: {e}")
        return None
    

def check_user_existence(user_id: int) -> bool:
    """Check if a user exists in the database.
       Return True if the user exists, False otherwise."""
    
    user_id = str(user_id)
    query = """
    SELECT user_id
    FROM users_data
    WHERE user_id = %s;
    """
    
    try:
        with connect_to_db() as connection_to_database:  
            with connection_to_database.cursor() as cursor:  
                cursor.execute(query, (user_id,))
                user = cursor.fetchone()
                
                if user:
                    print(f"[DATABASE INFO] User ID {user_id} exists in the database.")
                    return True
                
                else:
                    print(f"[DATABASE INFO] User ID {user_id} does not exist in the database.")
                    return False
        
    except Exception as e:
        print(f"[DATABASE ERROR] Failed to check user existence for ID {user_id}. Reason: {e}")
        return False
    

def delete_user(user_id: int) -> bool:
    """Delete a user from the database, from the users table.
       Return True if the user was deleted successfully or if the user is not found, False otherwise."""
        
    user_id = str(user_id)
    query = """
    DELETE FROM users_data
    WHERE user_id = %s;
    """

    try:
        with connect_to_db() as connection_to_database:  
            with connection_to_database.cursor() as cursor:  
                cursor.execute(query, (user_id,))
                
                if cursor.rowcount == 0:  # No rows found
                    print(f"[DATABASE INFO] User ID {user_id} does not exist. No action taken.")
                    return False
                
                else:
                    print(f"[DATABASE SUCCESS] User ID {user_id} deleted successfully.")
                    connection_to_database.commit()
                    return True
    
    except Exception as e:
        print(f"[DATABASE ERROR] Failed to delete user ID {user_id}. Reason: {e}")
        connection_to_database.rollback()
        return False
    

def set_user_chat_list(user_id: int, new_chats: list[tuple[str,int]]):
    """Update the chat for summary list of a user in the database, in the users table.
       Return True if the chat list was updated successfully, False otherwise."""
    
    user_id = str(user_id)
    query = """
    UPDATE users_data
    SET chats_to_summarize = %s
    WHERE user_id = %s;
    """

    try:
        with connect_to_db() as connection_to_database:  
            with connection_to_database.cursor() as cursor:  
                cursor.execute(query, (new_chats, user_id))
              
                if cursor.rowcount == 0:  # No rows found
                    print(f"[DATABASE INFO] User ID {user_id} does not exist. Chat list update skipped.")
                    return False
                
                else:
                    print(f"[DATABASE SUCCESS] Chat list for user ID {user_id} updated successfully to: {new_chats}")
                    connection_to_database.commit()
                    return True
    
    except Exception as e:
        print(f"[DATABASE ERROR] Failed to update chat list for user ID {user_id}. Reason: {e}")
        connection_to_database.rollback()
        return False
    

def get_user_chat_list(user_id: int) -> list[tuple[str,int]]:
    """return the chat for summary list of the user.
       Return Object if the chat list was fetched successfully or None otherwise."""
    
    user_id = str(user_id)
    query = """
    SELECT Chats_To_Summarize
    FROM users_data
    WHERE user_id = %s; 
    """

    try:
        with connect_to_db() as connection_to_database:  
            with connection_to_database.cursor() as cursor:  
                cursor.execute(query, (user_id,))
                chats_to_summarize = cursor.fetchone()

                if chats_to_summarize:
                    print(f"[DATABASE SUCCESS] Chat list for user ID {user_id} fetched successfully")
                    return chats_to_summarize
                
                else:
                    print(f"[DATABASE INFO] User ID {user_id} does not exist. Chat list fetching skipped.")
                    return None
    
    except Exception as e:
        print(f"[DATABASE ERROR] Failed to fetch Chat list for user ID {user_id}. Reason: {e}")
        return None
    

def set_user_time(user_id: int, new_time):
    """Update the time of a user summary in the database, in the users table."""
    
    user_id = str(user_id)
    query = """
    UPDATE users_data
    SET time_to_summarize = %s
    WHERE user_id = %s;
    """

    try:
        with connect_to_db() as connection_to_database:  
            with connection_to_database.cursor() as cursor:  
                cursor.execute(query, (new_time, user_id))

                if cursor.rowcount == 0:
                    print(f"[DATABASE INFO] User ID {user_id} does not exist. Time update skipped.")
                    return False
                
                else:
                    connection_to_database.commit()
                    print(f"[DATABASE SUCCESS] Time for user ID {user_id} updated successfully to: {new_time}")
                    return True
            
    except Exception as e:
        print(f"[DATABASE ERROR] Failed to update time for user ID {user_id}. Reason: {e}")
        return False


def get_user_time(user_id: int):
    """Return the time of summrizion for a given user
        return time is success else return None """

    user_id = str(user_id)
    query = """
    SELECT Chats_To_Summarize
    FROM users_data
    WHERE user_id = %s; 
    """

    try:
        with connect_to_db() as connection_to_database:
            with connection_to_database.cursor() as cursor:
                cursor.execute(query,(user_id,))
                time = cursor.fetchone()
                
                if time:
                    print(f"[DATABASE SUCCESS] time for summarizion of user ID {user_id} fetched successfully")
                    return time
                
                else:
                    print(f"[DATABASE INFO] User ID {user_id} does not exist. Chat list fetching skipped.")
                    return None
        
    except Exception as e:
        print(f"[DATABASE ERROR] Failed to fetch time of summarzion for user ID {user_id}. Reason: {e}")
        return None

