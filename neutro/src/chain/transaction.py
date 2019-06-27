"""transaction"""
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
        ("sender_address", str),
        ("receivers", List[str]),
        ("amounts", List[int]),
        ("nonce", int),
        ("fee", int),
        ("signature", str)
    ]

    def __init__(self, sender, receivers: List[str], amounts: List[int], nonce: int, fee: int, signature: str=""):
        # is sender wallet or string
        if isinstance(sender, Wallet):
            self.sender = sender
            self.sender_address = self.sender.address()
        elif isinstance(sender, str):
            self.sender_address = sender
        else:
            raise ValueError("sender must be Wallet or string")
        self.receivers = receivers
        self.amounts = amounts
        self.nonce = nonce
        self.fee = fee
        self.signature = signature
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
        """not the same as __hash__"""
        return hashutil.hash_string(self.string())

    def get_sender_address(self) -> str:
        """returns sender address"""
        return self.sender_address

    def unsigned_hash(self) -> str:
        """creates an unsigned transaction and returns a hash of it"""
        c = copy.copy(self)
        c.signature = ""
        return c.hash()

    def verify(self)-> bool:
        """
        verifies if this tx is signed by sender_address' private_key
        """
        return cryptoutil.verify_transaction_sig(self, self.signature)

    def get_signature(self) -> str:
        """returns the signature for this transaction"""
        return self.signature


def from_json_string(json_string: str) -> Transaction:
    """generates a transaction-object from a json-string"""
    _dict = json.loads(json_string)
    tx = Transaction(
        sender=_dict["sender_address"],
        receivers=_dict["receivers"],
        amounts=_dict["amounts"],
        nonce=_dict["nonce"],
        fee=_dict["fee"],
        signature=_dict["signature"]
    )
    return tx
