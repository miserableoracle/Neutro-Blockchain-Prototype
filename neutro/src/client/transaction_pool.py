
from neutro.src.util import loggerutil
from neutro.src.util import hashutil
from neutro.src.chain.transaction import Transaction


class TxPool():
    """this class implements a transaction pool and the required functionality"""

    def __init__(self):
        self.transactions = {}

    def get_transactions(self):
        """returns a list of json strings"""
        temp_list = []
        for t in self.transactions.values():
            temp_list += [t]
        return temp_list

    def get_size(self) -> int:
        return len(self.transactions)

    def add_transaction(self, transaction):
        if isinstance(transaction, Transaction):
            self.transactions[transaction.hash()] = transaction.string()
        elif isinstance(transaction, str):
            self.transactions[hashutil.hash_string(transaction)] = transaction
        else:
            loggerutil.error(
                "attempted to pool tx that was neither string nor Transaction object")

    def remove_transaction(self, transaction: Transaction):
        self.transactions.pop(transaction.hash(), None)
