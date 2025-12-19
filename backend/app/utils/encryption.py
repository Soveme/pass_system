from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
from app.config import settings

class DataEncryption:
    """Encrypt and decrypt sensitive data using AES-256"""
    
    def __init__(self, key: str = None):
        self.key = key or settings.encryption_key
        # Derive key from settings.encryption_key if needed
        if len(self.key) < 32:
            # Pad or hash the key to 32 bytes for AES-256
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'salt_pass_system',
                iterations=100000,
                backend=default_backend()
            )
            self.key = base64.urlsafe_b64encode(
                kdf.derive(self.key.encode())
            )
        else:
            self.key = base64.urlsafe_b64encode(self.key.encode()[:32])
        
        self.cipher = Fernet(self.key)
    
    def encrypt(self, data: str) -> str:
        """Encrypt string data"""
        try:
            encrypted = self.cipher.encrypt(data.encode())
            return encrypted.decode()
        except Exception as e:
            print(f"[ERROR] Encryption failed: {e}")
            return data
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt encrypted data"""
        try:
            decrypted = self.cipher.decrypt(encrypted_data.encode())
            return decrypted.decode()
        except Exception as e:
            print(f"[ERROR] Decryption failed: {e}")
            return encrypted_data

def encrypt_email(email: str) -> str:
    """Encrypt email address"""
    enc = DataEncryption()
    return enc.encrypt(email)

def decrypt_email(encrypted_email: str) -> str:
    """Decrypt email address"""
    enc = DataEncryption()
    return enc.decrypt(encrypted_email)

def encrypt_phone(phone: str) -> str:
    """Encrypt phone number"""
    enc = DataEncryption()
    return enc.encrypt(phone)

def decrypt_phone(encrypted_phone: str) -> str:
    """Decrypt phone number"""
    enc = DataEncryption()
    return enc.decrypt(encrypted_phone)
