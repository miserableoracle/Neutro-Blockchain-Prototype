"""class representing a Wallet and utils for this Wallet and Addresses"""
import logging
from typing import Tuple
from . import cryptoutil


class Wallet(object):
    """an address"""
    fields = [
        ("private_key", str),
        ("public_key", str),
    ]

    def __init__(self, private_key: str = None):
        """takes private_key or generates a new address"""
        logging.getLogger().debug("creating wallet")
        if private_key == None:
            self.private_key = cryptoutil.generate_priate_key()
        else:
            self.private_key = private_key
        self.public_key = cryptoutil.private_to_public(private_key)

    def __str__(self) -> str:
        """returns a HexString of this objects public_key"""
        return self.string()

    def __hash__(self) -> str:
        """returns a hash of self.__str__"""
        return self.hash()

    def get_private_key(self) -> str:
        """returns a HexString representation of self.private_key"""
        return self.private_key

    def get_public_key(self) -> str:
        """returns a HexString representation of self.public_key"""
        return self.public_key

    def hash(self) -> str:
        """same as __hash__"""
        cryptoutil.hash(self.string())

    def string(self) -> str:
        """same as __str__"""
        return self.public_key

    def sign(self, hex: str) -> Tuple[int, int, int]:
        """signs a hexString and returns v,r,s"""
        pass

    def address(self) -> str:
        return self.string()
