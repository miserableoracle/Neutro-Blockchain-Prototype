"""merkle trie for neutro chain"""
import logging


from typing import List
from util.types import Hash32, Uint


class Trie(object):
    """a merkle trie object"""

    fields = [
        (root_hash, HexString),
        (transactions, List[HexString])
    ]

    __init__(self, transactions=None: List[HexString]):
        logging.getLogger().debug("creating merkle-trie with:" + transactions)
        self.transactions = transactions
        self.root_hash = HexString()
        _calc_merkle_root()

    __str__(self) -> HexString:
        """returns the root_hash as HexString"""
        return self.string()

    def get_root(self) -> HexString:
        """returns a HexString containing root"""
        return self.root_hash

    def _calc_merkle_root():
        """private method that builds the merkle-trie and calculates root_hash"""
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
