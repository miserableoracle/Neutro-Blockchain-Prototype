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
            # save the new wallet
            wallet_database.save_wallet(
                self.address, self.private_key, self.public_key)
        else:
            # open existing wallet
            self.address = address
            self.private_key, self.public_key = wallet_database.open_wallet(
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

    def get_address(self):
        return self.address

    def sign(self, message: str) -> str:
        """sign a message with this wallet and return a strin of the signature"""
        digest = MD5.new(message.encode()).digest()
        return hex(self.private_key.sign(digest, 0)[0])[2:]

    def get_public_key(self):
        return self.public_key

    def verify(self, signature: str, message: str) -> bool:
        """verify that a message was signed with this wallet"""
        return verify(self.public_key, signature, message)


def verify(public_key, signature: str, message: str) -> bool:
    """verify that a message was signed with the public_keys private_key"""
    digest = MD5.new(message.encode()).digest()
    sig_tuple = (int(signature, 16), )
    return public_key.verify(digest, sig_tuple)
