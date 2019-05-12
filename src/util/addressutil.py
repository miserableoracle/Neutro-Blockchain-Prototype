"""class representing a Wallet and utils for this Wallet and Addresses"""
import logging


from .types import HexString
from . import cryptoutil


class Wallet(object):
    """an address"""
    fields = [
        (private_key, HexString)
        (public_key, HexString)
    ]

    def __init__(self, private_key: HexString = None):
        """takes private_key or generates a new address"""
        logging.getLogger().debug("creating wallet with:" + private_key)
        if private_key == None:
            self.private_key = cryptoutil.generate_priate_key()
        else:
            self.private_key = private_key
        self.public_key = cryptoutil.private_to_public(private_key)

    def __str__(self) -> HexString:
        """returns a HexString of this objects public_key"""
        return self.string()

    def __hash__(self) -> HexString:
        """returns a hash of self.__str__"""
        return self.hash()

    def get_private_key(self) -> HexString:
        """returns a HexString representation of self.private_key"""
        return self.private_key

    def get_public_key(self) -> HexString:
        """returns a HexString representation of self.public_key"""
        return self.public_key

    def hash(self) -> HexString:
        """same as __hash__"""
        cryptoutil.hash(self.string())

    def string(self) -> HexString:
        """same as __str__"""
        return self.public_key
