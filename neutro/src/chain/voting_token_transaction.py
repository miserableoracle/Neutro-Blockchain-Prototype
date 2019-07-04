"""class representing a transaction to give voting power from a to b"""
import json
import copy
from typing import List
from neutro.src.util import loggerutil
from neutro.src.util import wallet
from neutro.src.util.wallet import Wallet
from neutro.src.util import hashutil
from neutro.src.util import stringutil
from neutro.src.util import cryptoutil


class VotingTokenTransaction(object):
    """
    VotingTokenTransaction
    a transaction signed by sender and reciever

    what this dose is send voting tokens from sender to reciever, 
    and neutro from receiver to sender, so both have to sign this 
    before it can be incorporated into a block
    """

    fields = [
        ("sender_address", str),
        ("receiver_address", str),
        ("vt_amount", int),
        ("nto_amount", int),
        ("sender_nonce", int),
        ("receiver_nonce", int),
        ("sender_signature", str),
        ("receiver_signature", str)
    ]

    def __init__(self, sender: str, receiver: str, vt_amount: int, nto_amount: int):
        self.sender_address = sender
        self.receiver_address = receiver
        self.vt_amount = vt_amount
        self.nto_amount = nto_amount
        self.sender_nonce = sender_nonce
        self.receiver_nonce = receiver_nonce
        self.sender_signature = sender_signature
        self.receiver_signature = receiver_signature
        loggerutil.debug("creating VotingTokenTransaction: " + self.string())

    def __str__(self) -> str:
        """returns a JsonString of itself"""
        return self.string()

    def __hash__(self) -> int:
        """returns an int as hash of this object"""
        return int(self.hash(), 16)

    def string(self) -> str:
        """same as __str__"""
        ret = {}
        for f in self.fields:
            ret.update({f[0]: getattr(self, f[0])})
        return stringutil.dict_to_string(ret)

    def hash(self) -> str:
        """returns a hex string of the hash of this object"""
        return hashutil.hash_string(self.string())

    def get_sender_address(self) -> str:
        """returns sender address"""
        return self.sender_address

    def get_receiver_address(self) -> str:
        """returns receiver address"""
        return self.receiver_address

    def unsigned_hash(self) -> str:
        """creates an unsigned transaction and returns a hash of it"""
        c = copy.copy(self)
        c.sender_signature = ""
        c.receiver_signature = ""
        return c.hash()

    def get_sender_signature(self) -> str:
        return self.sender_signature

    def get_receiver_signature(self) -> str:
        return self.receiver_signature

    def verify_sender_sig(self) -> bool:
        try:
            return cryptoutil.verify_transaction_sig(self, self.sender_signature, self.sender_address)
        except AssertionError:
            return False

    def verify_receiver_sig(self) -> bool:
        try:
            return cryptoutil.verify_transaction_sig(self, self.receiver_signature, self.receiver_address)
        except AssertionError:
            return False

    def verify(self) -> bool:
        return self.verify_sender_sig() and self.verify_receiver_sig()


def from_json_string(json_string: str) -> VotingTokenTransaction:
    """generates a transaction-object from a json-string"""
    _dict = json.loads(json_string)
    vt_tx = VotingTokenTransaction(
        sender=_dict["sender_address"],
        receiver=_dict["receiver_address"],
        vt_amount=_dict["vt_amount"],
        nto_amount=_dict["nto_amount"],
        sender_signature=_dict["sender_signature"],
        receiver_signature=_dict["receiver_signature"]
    )
    return vt_tx
