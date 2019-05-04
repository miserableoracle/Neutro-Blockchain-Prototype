"""class representing an address and utils for this address"""
import base58
from .util.types import Hash32, Uint, PrivateKey, PublicKey

from .util import cryptoutil


class Address(object):
    """an address"""
    fields = [
        (private_key, PrivateKey)
        (public_key, PublicKey)
    ]

    def __init__(self, private_key=None: PrivateKey):
        """takes private_key or generates a new address"""
        if private_key == None:
            self.private_key = cryptoutil.generate_priate_key()
        else:
            self.private_key = private_key
        self.public_key = cryptoutil.private_to_public(private_key)

    def __str__(self) -> str:
        return self.string()

    def __hash__(self) -> Hash32:
        return self.hash()

    def get_private_key(self) -> PrivateKey:
        return self.private_key

    def get_public_key(self) -> PublicKey:
        return self.public_key

    def hash(self) -> Hash32:
        pass

    def string(self) -> str:
        return base58.b58encode(self.public_key)


def address_from_str(address: str) -> Address:
    pass  # dont even know if that should be possible?!


address = Address()
