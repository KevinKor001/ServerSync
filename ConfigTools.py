from logging import Manager
import os
from lib.cryptography.fernet import Fernet

class CredentialManager:
    def __init__(self, key_file="secret_key"):
        self.key_file = key_file
        self.key = self._load_or_generate_key()
        self.cipher = Fernet(self.key)
    
    def _load_or_generate_key(self):
        if not os.path.exists(self.key_file):
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as file:
                file.write(key)
            os.chmod(self.key_file, 0o600)
            return key
        with open(self.key_file, "rb") as file:
            return file.read()

    def encrypt_password(self, password):
        return self.cipher.encrypt(password.encode()).decode()

    def dencrypt_password(self, encrypted_password):
        return self.cipher.decrypt(encrypted_password.encode()).decode()


manager = CredentialManager()

password = "test1"
encrypted = manager.encrypt_password(password)
print(f"encrpted: {encrypted}")


decripted = manager.dencrypt_password(encrypted)
print(f"Decripted: {decripted}")













