"""class representing a block"""
import time
import json
from typing import List
from neutro.src.util import loggerutil
from neutro.src.util import hashutil
from neutro.src.util import stringutil
from neutro.src.trie.trie import Trie
from neutro.src.chain.transaction import Transaction
from neutro.src.chain.vote import Vote
from neutro.src.database import block_database
from neutro.src.database import peer_block_database


class Block(object):
    """class representing a block"""
    fields = [
        ("prev_hash", str),
        ("tx_merkle_root", str),
        ("transactions", List[str]),
        ("miner", str),
        ("height", int),
        ("difficulty", str),
        ("reward", str),
        ("nonce", str),
        ("tx_count", int),
        ("time", int)
    ]

    def __init__(self, prev_hash: str, transactions: List[str], miner: str, difficulty: str, nonce: str):
        self.prev_hash = prev_hash
        self.transactions = transactions
        self.miner = miner
        try:
            self.height = block_database.get_current_height() + 1
            self.height_peer = peer_block_database.get_current_height() + 1
        except:
            self.height = 0
            self.height_peer = 0
        self.difficulty = difficulty
        self.nonce = nonce
        self.reward = "00"
        if not transactions or len(transactions) == 0:
            self.transactions = []
            self.tx_count = 0
            self.tx_merkle_root = stringutil.empty_root
        else:
            trie = Trie(transactions)
            self.tx_count = trie.size()
            self.tx_merkle_root = trie.root()
        self.time = int(time.time() * 1000.0)

        loggerutil.debug("created block: " + self.string())

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

    def get_tx_root(self) -> str:
        """returns the tx_merkle_root of this block"""
        return self.tx_merkle_root

    def get_heigth(self) -> int:
        """returns the height of this block"""
        return self.height

    def get_height_peer(self):
        """returns the height of this block - peer case"""
        return self.height_peer

    def save(self):
        """saves this block to local database"""
        block_database.save_block(self.height, self.string(), self.hash())

    def peer_save(self):
        """saves this block to local database"""
        peer_block_database.save_block(self.height_peer, self.string(), self.hash())


def from_json_string(json_block: str) -> Block:
    """generates a block-object from a json-string"""
    _dict = json.loads(json_block)
    block = Block(
        prev_hash=_dict["prev_hash"],
        transactions=_dict["transactions"],
        miner=_dict["miner"],
        difficulty=_dict["difficulty"],
        nonce=_dict["nonce"]
    )
    block.height = int(_dict["height"])
    block.time = _dict["time"]
    return block
