"""class representing a Wallet and utils for this Wallet and Addresses"""
import ecdsa

from neutro.src.util import loggerutil
from neutro.src.util import hashutil
from neutro.src.util import stringutil
from neutro.src.util import cryptoutil


class Wallet(object):
    """basically just a wrapper for a private key with functionality for signing"""
    fields = [
        ("address", str),
        ("nonce", int)
    ]

    def __init__(self, private_key: ecdsa.SigningKey, nonce: int):
        """
        wraps a private key to represent a wallet
        """
        self.private_key = private_key
        self.public_key = self.private_key.get_verifying_key()
        self.address = cryptoutil.key_to_address(self.public_key)
        self.nonce = nonce

    def __str__(self) -> str:
        """returns a JsonString of itself"""
        return self.string()

    def string(self) -> str:
        """returns a JsonString of itself"""
        ret = {}
        for f in self.fields:
            ret.update({f[0]: getattr(self, f[0])})
        return stringutil.dict_to_string(ret)

    def get_address(self) -> str:
        return self.address

    def get_nonce(self) -> int:
        return self.nonce

    def get_public_key(self):
        return self.public_key

    def get_private_key(self):
        return self.private_key

    def sign_vote(self, vote):
        """signes a vote with this wallet"""
        if vote.get_sender() != self.get_address():
            raise ValueError(
                "cannot sign vote where v.sender is different to this wallets address")
            loggerutil.info("could not sign vote " +
                            vote.string() + " with wallet " + self.string())
        vote.signature = cryptoutil.get_vote_sig(self.get_private_key(), vote)

    def sign_transaction(self, transaction):
        """
        signes the transaction with this wallet. Also updating the nonce.
        """
        if transaction.get_sender() != self.get_address():
            raise ValueError(
                "cannot sign transaction where tx.sender is different to this wallets address")
            loggerutil.info("could not sign transaction " +
                            transaction.string() + " with wallet " + self.string())
        transaction.nonce = self.nonce
        # update and save nonce
        self.nonce += 1

        # set tx signature
        transaction.signature = cryptoutil.get_transaction_sig(
            self.get_private_key(), transaction)

    def sign_vtx_sender(self, vtx):
        """signs a voting token transaction with this wallet as sender"""
        if vtx.get_sender() != self.get_address():
            raise ValueError(
                "cannot sign vtx where tx.sender is different to this wallets address")
            loggerutil.info("could not sign vtx as sender" +
                            vtx.string() + " with wallet " + self.string())
        vtx.sender_nonce = self.nonce
        # update and save nonce
        self.nonce += 1

        # set tx signature
        vtx.sender_signature = cryptoutil.get_transaction_sig(
            self.get_private_key(), vtx)

    def sign_vtx_receiver(self, vtx):
        """signs a voting token transaction with this wallet as receiver"""
        if vtx.get_receiver() != self.get_address():
            raise ValueError(
                "cannot sign vtx where tx.receiver is different to this wallets address")
            loggerutil.info("could not sign vtx as receiver" +
                            vtx.string() + " with wallet " + self.string())
        vtx.receiver_nonce = self.nonce
        # update and save nonce
        self.nonce += 1

        # set tx signature
        vtx.receiver_signature = cryptoutil.get_transaction_sig(
            self.get_private_key(), vtx)


def generate_new_wallet() -> Wallet:
    return Wallet(cryptoutil.generate_key(), 0)
