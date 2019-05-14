"""utils for managing crypto"""
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from .types import HexString
from src.chain.transaction import Transaction


class Cryptoutil(object):
    """
    public/private key pair
    """

    def __init__(self):
        self.signer = PKCS1_v1_5.new(self.generate_priate_key())

    def generate_priate_key() -> HexString:
        random_generator = Crypto.Random.new().read
        return RSA.generate(1024, random_generator)

    def private_to_public(self, private_key: bytes) -> HexString:
        return private_key.publickey()

    def sign(self, message):
        """
        Sign a message
        """
        hashed = SHA.new(message.encode('utf8'))
        return binascii.hexlify(self.signer.sign(hashed)).decode('ascii')

    def sign_transaction(self, tx: Transaction, )
