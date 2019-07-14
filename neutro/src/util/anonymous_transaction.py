from neutro.src.chain.transaction import Transaction
from typing import List
from neutro.src.util import cryptoutil
from neutro.src.util import hashutil
from neutro.src.util import stringutil
import cryptography
from cryptography.fernet import Fernet


class AnonymousTransaction(Transaction):
    pass

    def generate_key(self) -> bytes:
        """ generates a new random key"""
        key = Fernet.generate_key()
        return key

    def store_key(self):
        """create/overwrite a file with the key in it"""
        key = self.generate_key()
        file = open('key.key', 'wb')
        file.write(key)
        file.close()

    def read_stored_key(self):
        """reads the stored key"""
        file = open('key.key', 'rb')
        key = file.read(key)  # The key will be type bytes
        file.close()

    def encrypt(self, key: bytes, message: bytes) -> bytes:
        """encrypts a byte message using the symmetric key"""
        f = Fernet(key)
        encrypted = f.encrypt(message)
        return encrypted

    def decrypt(self, key: bytes, encrypted_message: bytes) -> bytes:
        f = Fernet(key)
        decrypted_message = f.decrypt(encrypted_message)
        return decrypted_message






