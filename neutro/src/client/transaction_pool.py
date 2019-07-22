"""
implements a transaction pool based on a 
dict(hash:transaction)
"""
from neutro.src.util import loggerutil


class TransactionPool(object):
    """this class implements a transaction pool and the required functionality"""

    def __init__(self):
        self.transactions = {}

    def get_tx_list(self):
        """returns a list Transactions"""
        temp_list = []
        for t in self.transactions.values():
            temp_list += [t]
        return temp_list

    def get_size(self) -> int:
        """returns the size of the pool"""
        return len(self.transactions)

    def add(self, transaction):
        """
        adds a transaction to the pool
        this is not 100% correct because theoretically 2 diferent entities 
        could have the same hash, but in that case the whole concept of 
        Blockchain breaks, so this is of no relevance for now
        """
        try:
            self.transactions[transaction.hash()]
        except:
            self.transactions[transaction.hash()] = transaction

    def get_by_hash(self, transaction_hash):
        """returns tx by hash"""
        try:
            return self.transactions[transaction_hash]
        except:
            return None

    def remove(self, transaction):
        """removes a transaction from the pool"""
        self.transactions.pop(transaction.hash(), None)
