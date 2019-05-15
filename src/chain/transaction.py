"""transaction"""
import logging
from typing import List
from src.util.types import HexString
from src.util.addressutil import Wallet


class Transaction(object):
    """an Object representing a transaction dict of HexString"""
    fields = [
        ("sender", Wallet),
        ("signature", HexString),
        ("receivers", List[HexString]),
        ("amounts", List[HexString]),
        ("nonce", HexString),
        ("fee", HexString),
    ]

    def __init__(self, sender: Wallet, receivers: List[HexString], amounts: List[HexString], nonce: HexString, fee: HexString, v=0, r=0, s=0):
        logging.getLogger().debug("creating transaction with:" + sender + " " /
                                  + receivers + " " + amounts + " " + nonce + " " + fee)
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

    def __hash__(self) -> HexString:
        """returns a HexString of hash(self.__str__())"""
        return self.hash()

    def string(self) -> str:
        """same as __str__"""
        pass

    def hash(self) -> HexString:
        """same as __hash__"""
        pass

    def sign(self, private_key: HexString) -> Transaction:
        raw_hash = self.hash()
        v, r, s = sender.sign(raw_hash)
        return self.copy(v=v, r=r, s=s)


def get_hashes_list(transactions: List[Transaction]) -> List[HexString]:
    """takes a list of Transaction objects and returns a list of HexString containing hash(tx) for each tx"""
    return [tx.hash() for tx in transactions]
