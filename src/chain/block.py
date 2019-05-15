"""class representing a block"""

import json
from typing import List
from src.util import loggerutil
from src.util import hashutil
from src.util import stringutil


class Block(object):
    """class representing a block"""
    fields = [
        ("prev_hash", str),
        ("tx_merkle_root", str),
        ("miner", str),
        ("difficulty", str),
        ("reward", str),
        ("nonce", str),
        ("tx_count", int)
    ]

    def __init__(self, prev_hash: str, tx_merkle_root: str, miner: str, difficulty: str, nonce: str, tx_count: int):
        self.prev_hash = prev_hash
        self.tx_merkle_root = tx_merkle_root
        self.miner = miner
        self.difficulty = difficulty
        self.nonce = nonce
        self.tx_count = tx_count
        self.reward = "00"

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
        return stringutil.dict_to_string(ret)

    def hash(self) -> str:
        """same as __hash__"""
        return hashutil.hash_string(self.string())
