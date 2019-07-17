"""
implements a transaction pool based on a 
dict(hash:transaction)
"""
from neutro.src.util import loggerutil
from neutro.src.util import hashutil
from neutro.src.chain.transaction import Transaction


class TxPool():
    """this class implements a transaction pool and the required functionality"""

    def __init__(self):
        self.transactions = {}

    def get_transactions(self):
        """returns a list Transactions"""
        temp_list = []
        for t in self.transactions.values():
            temp_list += [t]
        return temp_list

    def get_size(self) -> int:
        """returns the size of the pool"""
        return len(self.transactions)

    def add_transaction(self, transaction: Transaction):
        """adds a transaction to the pool"""
        if isinstance(transaction, Transaction):
            self.transactions[transaction.hash()] = transaction
        else:
            loggerutil.error(
                "attempted to pool tx that was neither string nor Transaction object")

    def get_transaction_by_hash(self, _hash: str):
        """returns a transaction by hash"""
        return self.transactions[_hash]

    def remove_transaction(self, transaction: Transaction):
        """removes a transaction from the pool"""
        self.transactions.pop(transaction.hash(), None)

    def remove_transaction_by_hash(self, _hash: str):
        """removes a transaction from the pool"""
        self.transactions.pop(_hash, None)
