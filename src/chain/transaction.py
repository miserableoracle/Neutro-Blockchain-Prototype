"""transaction"""
import logging
import json
from typing import List
from src.util.wallet import Wallet


class Transaction(object):
    """an Object representing a transaction dict of HexString"""
    fields = [
        ("sender", Wallet),
        ("receivers", List[str]),
        ("amounts", List[int]),
        ("nonce", int),
        ("fee", int),
        ("v", int),
        ("r", int),
        ("s", int),
    ]

    def __init__(self, sender: Wallet, receivers: List[str], amounts: List[int], nonce: int, fee: int, v=0, r=0, s=0):
        logging.getLogger().debug("creating transaction")
        self.sender = sender
        self.receivers = receivers
        self.amounts = amounts
        self.nonce = nonce
        self.fee = fee
        self.v = v
        self.r = r
        self.s = s

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
        return json.dumps(ret)

    def hash(self) -> str:
        """same as __hash__"""
        return hashutil.hash_string(self.string())

    def sign(self, private_key: str):
        raw_hash = self.hash()
        self.v, self.r, self.s = sender.sign(raw_hash)


def get_hashes_list(transactions: List[Transaction]) -> List[str]:
    """takes a list of Transaction objects and returns a list of HexString containing hash(tx) for each tx"""
    return [tx.hash() for tx in transactions]
