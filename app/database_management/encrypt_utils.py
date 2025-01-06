import os
import dotenv
from cryptography.fernet import Fernet


dotenv.load_dotenv()


def get_key() -> bytes:
    """get the encryption key"""

    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
    if not ENCRYPTION_KEY:
        print("[ERROR] The encryption key is missing. Please set it in the .env file.")
        return None
    return ENCRYPTION_KEY.encode()


def encrypt_data(data: str) -> bytes:
    """Encrypt the data using the encryption key"""

    byte_key = get_key()
    cipher_suite = Fernet(byte_key)
    return cipher_suite.encrypt(data.encode())


def decrypt_data(data: bytes) -> str:
    """Decrypt the data using the encryption key"""

    byte_key = get_key()
    cipher_suite = Fernet(byte_key)
    return cipher_suite.decrypt(data).decode()