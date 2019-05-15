"""merkle trie for neutro chain"""
import json
from typing import List

from src.util import hashutil
from src.util import loggerutil
from src.util import stringutil

# define a default hash for empty subtree roots
empty_root = hashutil.hash_string("00")


class Trie(object):
    """a merkle trie object"""

    fields = [
        ("root_hash", str),
        ("_size", int),
        ("transactions", List[str])
    ]

    def __init__(self, transactions: List[str] = None):
        self.transactions = transactions
        self.root_hash = empty_root
        if transactions:
            self._size = len(self.transactions)
            calc_merkle_root(self)
        else:
            self._size = 0
        loggerutil.debug("creating merkle-trie with:" + self.string())

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
        return stringutil.dict_to_string(ret).replace("_size", "size")

    def hash(self) -> str:
        """same as __hash__"""
        return hashutil.hash_string(self.string())

    def root(self) -> str:
        """returns a HexString containing root"""
        return self.root_hash

    def size(self) -> int:
        """reutns an int of the number of tx in this tie"""
        return self._size

    def transactions_list(self) -> str:
        """returns a string of the transaction dict"""
        return stringutil.dict_to_string(self.transactions)


def calc_merkle_root(trie):
    """private method that builds the merkle-trie and calculates root_hash"""
    txs = trie.transactions.copy()
    # do until there is only one hash left
    while len(txs) != 1:
        temp = []
        # add an empty hash if the number of hashes is unequal
        if len(txs) % 2 == 1:
            txs.append(empty_root)
        # go over all pairs and hash them
        for tup in zip(txs[0::2], txs[1::2]):
            temp.append(hashutil.hash_tuple(tup[0], tup[1]))
        # continue with new result
        txs = temp
    # set root and finihs
    trie.root_hash = txs[0]
