"""class representing a shard block"""
import time
import json
from typing import List
from neutro.src.util import loggerutil
from neutro.src.util import hashutil
from neutro.src.util import stringutil
from neutro.src.trie.trie import Trie
from neutro.src.chain import transaction
from neutro.src.chain.transaction import Transaction
from neutro.src.database import block_database


class ShardBlock(object):
    """a class representing a shard/sub block in the neutro Blockchain"""
    fields = [
        ("prev_main_hash", str),
        ("prev_shard_hash", str),
        ("height", int),
        ("time", int),
        ("miner", str),

        ("tx_merkle_root", str),
        ("tx_list", str),
        ("tx_count", int)
    ]

    def __init__(self, prev_main_hash: str, prev_shard_hash: str, miner: str, tx_list: List[Transaction]):
        self.prev_main_hash = prev_main_hash
        self.prev_shard_hash = prev_shard_hash
        self.height = 0  # TODO
        self.miner = miner
        self.time = int(time.time() * 1000)

        if not tx_list or len(tx_list) == 0:
            self.tx_list = []
        else:
            self.tx_list = tx_list
        self.trie = Trie([tx.hash() for tx in self.tx_list])
        self.tx_count = self.trie.size()
        self.tx_merkle_root = self.trie.root()

        loggerutil.debug("created ShardBlock: " + self.string())

    def __str__(self) -> str:
        """returns a json-string of itself without the transaction list"""
        return self.string()

    def __hash__(self) -> int:
        """returns an int as hash of this object"""
        return int(self.hash(), 16)

    def string(self, with_transaction_list=False) -> str:
        """
        returns a json-string of itself

        with_transaction_list is there to store and boradcast a
        shard-block containing all information
        """
        ret = {}
        for f in self.fields:
            ret.update({f[0]: getattr(self, f[0])})
        if not with_transaction_list:
            ret.pop("tx_list", None)
        else:
            ret["tx_list"] = [tx.string() for tx in ret["tx_list"]]
        return stringutil.dict_to_string(ret)

    def hash(self) -> str:
        """returns a hex string of the hash of this object"""
        return hashutil.hash_string(self.string())

    def get_tx_root(self) -> str:
        """returns the tx_merkle_root of this block"""
        return self.tx_merkle_root

    def get_heigth(self) -> int:
        """returns the height of this block"""
        return self.height


def from_json(json_block: str) -> ShardBlock:
    """generates a block-object from a json-string"""
    _dict = json.loads(json_block)
    try:
        tx_list = [transaction.from_json(tx) for tx in _dict["tx_list"]]
    except KeyError:
        tx_list = []

    block = ShardBlock(
        prev_main_hash=_dict["prev_main_hash"],
        prev_shard_hash=_dict["prev_shard_hash"],
        miner=_dict["miner"],
        tx_list=tx_list
    )
    block.height = _dict["height"]
    block.time = _dict["time"]

    return block
