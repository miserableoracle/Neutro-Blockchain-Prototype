"""class representing a Wallet and utils for this Wallet and Addresses"""
import json
import base58
import ecdsa
import binascii

from src.util import loggerutil
from src.util import hashutil
from src.util import stringutil
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
            self.private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
            self.public_key = self.private_key.get_verifying_key()
            self.address = key_to_address(self.public_key)
            self.nonce = 0
            # save the new wallet
            self.save()
        else:
            # open existing wallet
            self.address = address
            self.public_key = address_to_key(address)
            self.private_key, self.nonce = wallet_database.open_wallet(
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
        return str(binascii.hexlify(
            self.private_key.sign(message.encode("utf-8"))))[2:-1]

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

    def get_private_key(self):
        return self.private_key

    def verify(self, signature: str, message: str) -> bool:
        """verify that a message was signed with this wallet"""
        return self.public_key.verify(binascii.unhexlify(signature), message.encode("utf-8"))

    def save(self):
        """saves this wallet to local files"""
        wallet_database.save_wallet(self.address, self.private_key, self.nonce)


def key_to_address(public_key: ecdsa.VerifyingKey) -> str:
    """returns a b58 encoded version of the public_key"""
    return str(base58.b58encode(public_key.to_string()))[2:-1]


def address_to_key(address: str) -> ecdsa.VerifyingKey:
    """returns a public key, decoded from the address"""
    return ecdsa.VerifyingKey.from_string(bytes.fromhex(binascii.hexlify(
        base58.b58decode(address)).decode('utf-8')), curve=ecdsa.SECP256k1)


def verify_transaction_sig(transaction) -> bool:
    """verifys that a given transaction is signed with senders private key"""
    address = transactions.get_sender_address()
    signature = transaction.get_signature()
