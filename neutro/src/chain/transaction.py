"""class representing a transaction"""
import json
import copy
from typing import List
from neutro.src.util import loggerutil
from neutro.src.util import wallet
from neutro.src.util.wallet import Wallet
from neutro.src.util import hashutil
from neutro.src.util import stringutil
from neutro.src.util import cryptoutil


class Transaction(object):
    """an Object representing a transaction"""
    fields = [
        ("sender", str),
        ("receivers", List[str]),
        ("amounts", List[int]),
        ("nonce", int),
        ("fee", int),
        ("signature", str)
    ]

    def __init__(self, sender: str, receivers: List[str], amounts: List[int], fee: int):
        self.sender = sender
        self.receivers = receivers
        self.amounts = amounts
        self.fee = fee
        self.nonce = 0
        self.signature = ""
        loggerutil.debug("creating transaction: " + self.string())

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

    def get_sender(self) -> str:
        """returns sender address"""
        return self.sender

    def unsigned_hash(self) -> str:
        """creates an unsigned transaction and returns a hash of it"""
        c = copy.copy(self)
        c.signature = ""
        return c.hash()

    def verify(self)-> bool:
        """
        verifies if this tx is signed by sender' private_key
        """
        try:
            return cryptoutil.verify_transaction_sig(self, self.signature)
        except AssertionError:
            return False

    def get_signature(self) -> str:
        """returns the signature for this transaction"""
        return self.signature


def from_json(json_string: str) -> Transaction:
    """generates a transaction-object from a json-string"""
    _dict = json.loads(json_string)
    tx = Transaction(
        sender=_dict["sender"],
        receivers=_dict["receivers"],
        amounts=_dict["amounts"],
        fee=_dict["fee"]
    )
    tx.nonce = _dict["nonce"]
    tx.signature = _dict["signature"]
    return tx
