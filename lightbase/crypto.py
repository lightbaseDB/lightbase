import hashlib
import os

from typing import Any

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

from pymongo import MongoClient


class Crypto:
    """
    # Crypto

    ---
    Parameters:
        - MongoUrl: str
            Url to connect to the database

        - Database: str
            Database name

        - Collection: str
            Collection name

    Methods:
        - salt(data: Any) -> None
            Salting data
        - encrypt(data: Any, password: str) -> None
            Encrypting data
        - decrypt(password: str) -> None
            Decrypting data

    """

    def __init__(
        self,
        MongoUrl: str,
        Database: str,
        Collection: str

    ) -> None:
        self.client = MongoClient(MongoUrl)

        if not self.client:
            raise Exception("Error connecting to the database")
        
        self._db = self.client[Database]
        self._collection = self._db[Collection]
        
    def salt(self, data: dict) -> None:
        """
        # Salting

        ---
        Parameters:
            - data: Any
                Data to salt

        Returns:
            - salted_message: bytes
                Salted data
        """
        for i in data:
            salted_message = os.urandom(16) + str(i).encode("utf-8")

        hashed_message = hashlib.sha256(salted_message).hexdigest()

        return hashed_message

    def encrypt(self, data: dict, password: str) -> None:
        """
        # Encrypting

        ---
        Parameters:
            - data: Any
                Data to encrypt
            - password: str
                Password to encrypt data
        Returns:
            - encrypted_data: bytes
                Encrypted data
            - tag: bytes
                Tag to verify data
        """
        salt_password = PBKDF2(password, self.salt(password), dkLen=32)
        salt_data = self.salt(data).encode("utf-8")

        cipher = AES.new(salt_password, AES.MODE_EAX)

        encrypted_data, tag = cipher.encrypt_and_digest(salt_data)

        self._collection.insert_one({
            encrypted_data
        })

        return "lol"

    # def decrypt(self, password: str) -> None:
    #     """
    #     # Decrypting

    #     ---
    #     Parameters:
    #         - file: str
    #             File to decrypt
    #         - password: str
    #             Password to decrypt data

    #     Returns:
    #         - decrypted_data: bytes
    #             Decrypted data
    #     """
    #     salt_password = PBKDF2(password, self.salt(password), dkLen=32)

    #     cipher = AES.new(salt_password, AES.MODE_EAX)

    #     decrypted_data = cipher.decrypt(encrypted_data)

    #     return decrypted_data
    
test = Crypto("mongodb://localhost:27017/", "test", "test")

print(test.encrypt({"test", "test"}, "test"))