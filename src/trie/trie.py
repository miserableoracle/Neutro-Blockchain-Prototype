"""merkle trie for neutro chain"""
from typing import List
from util.types import Hash32, Uint


class Trie(object):
    """a merkle trie object"""

    fields = [
        (root, Hash32),
        (transactions, List[Hash32]),
        (nonce, Uint)
    ]

    __init__(self, transactions=None: List[Hash32]):
        self.transactions = transactions
        self.root_hash = Hash32()
        _calc_merkle_root()

    __str__(self):
        return self.string()

    def get_root(self) -> Hash32:
        return self.root_hash

    def _calc_merkle_root():
        txs = self.transactions.copy()
        # do until there is only one hash left
        while len(txs) != 1:
            temp = []
            # add an empty hash if the number of hashes is unequal
            if len(txs) % 2 == 1:
                txs.append(Hash32())
            # go over all pairs and hash them
            for tup in zip(txs[0::2], txs[1::2]):
                temp.append(Hash32(tup[0]).update(tup[1]))
            # continue with new result
            txs = temp
        # set root and finihs
        self.root_hash = txs[0]
