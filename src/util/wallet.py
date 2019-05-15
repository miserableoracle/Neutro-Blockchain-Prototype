"""class representing a Wallet and utils for this Wallet and Addresses"""
from Crypto.PublicKey import RSA
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
            wallet_database.save(
                self.address, self.private_key, self.public_key)
        else:
            # open existing wallet
            self.private_key, self.public_key = wallet_database.open(address)
            self.address = address

    def __str__(self) -> str:
        """returns a JsonString of itself"""
        return self.string()

    def __hash__(self) -> str:
        """returns a HexString of hash(self.__str__())"""
        return self.hash()

    def string(self) -> str:
        """same as __str__"""
        ret = {}
        for f in self.fields:
            ret.update({f[0]: getattr(self, f[0])})
        return stringutil.dict_to_string(ret)

    def hash(self) -> str:
        """same as __hash__"""
        return hashutil.hash_string(self.string())
