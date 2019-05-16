"""class representing a Wallet and utils for this Wallet and Addresses"""
from Crypto.PublicKey import RSA
from Crypto.Hash import MD5
import json

from src.util import loggerutil
from src.util import hashutil
from src.util import stringutil
from src.util import cryptoutil
from src.database import wallet_database


class Wallet(object):
    """an address"""
    fields = [
        ("address", str)
    ]

    def __init__(self, address: str = None):
        """
        either generates a new wallet and saves it
        or takes an address and opens a wallet file for this address
        """
        if not address:
            self.private_key = RSA.generate(1024)
            self.public_key = self.private_key.publickey()
            self.address = hashutil.hash_bytes(
                self.public_key.exportKey(format="OpenSSH"))
            self.nonce = 0
            # save the new wallet
            self.save()
        else:
            # open existing wallet
            self.address = address
            self.private_key, self.public_key, self.nonce = wallet_database.open_wallet(
                self.address)

    def __str__(self) -> str:
        """returns a JsonString of itself"""
        return self.string()

    def string(self) -> str:
        """same as __str__"""
        ret = {}
        for f in self.fields:
            ret.update({f[0]: getattr(self, f[0])})
        return stringutil.dict_to_string(ret)

    def get_address(self) -> str:
        return self.address

    def get_nonce(self) -> int:
        return self.nonce

    def sign_message(self, message: str) -> str:
        """sign a message with this wallet and return a strin of the signature"""
        digest = MD5.new(message.encode()).digest()
        return hex(self.private_key.sign(digest, 0)[0])[2:]

    def sign_transaction(self, transaction) -> str:
        """
        signs a given transaction with this wallet.
        if transaction.sender != self.address() a new value error is raised
        returns signature hex-string and nonce for the tx
        """
        if not transaction.get_sender_address() == self.get_address():
            raise ValueError("transaction (" + transaction.string() +
                             ") cannot be signed with " + self.get_address())
            loggerutil.error("transaction (" + transaction.string() +
                             ") cannot be signed with " + self.get_address())
        else:
            # nonces are there to determine the order of transactions signed by this wallet.
            # this prevents double spending
            transaction.nonce = self.nonce
            self.nonce += 1
            # this can be spead up by just saving the nonce.
            # TODO after prototype
            self.save()

            unsigned_hash = transaction.unsigned_hash()
            return self.sign_message(unsigned_hash)

    def get_public_key(self):
        return self.public_key

    def verify(self, signature: str, message: str) -> bool:
        """verify that a message was signed with this wallet"""
        return verify(self.public_key, signature, message)

    def save(self):
        """saves this wallet to local files"""
        wallet_database.save_wallet(
            self.address, self.private_key, self.public_key, self.nonce)


def verify(public_key, signature: str, message: str) -> bool:
    """verify that a message was signed with the public_keys private_key"""
    digest = MD5.new(message.encode()).digest()
    sig_tuple = (int(signature, 16), )
    return public_key.verify(digest, sig_tuple)
