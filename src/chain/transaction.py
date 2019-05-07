"""transaction"""
import logging

from typing import List
from util.types import HexString


class Transaction(object):
"""an Object representing a transaction dict of HexString"""
	fields = [
		(sender, HexString),
		(signature, HexString),
		(receivers, List[HexString]),
		(amounts, List[HexString]),
		(nonce, HexString),
		(fee, HexString)
	]
    __init__(self, sender: HexString, receivers: List[HexString], amounts: List[HexString], nonce: HexString, fee:HexString):
    	logging.getLogger().debug("creating transaction with:" + sender + " " /
            + receivers + " " + amounts + " " + nonce + " " + fee)
        self.sender = sender
    	self.signature = Wallet(sender).get_transaction_sig()
    	self.receivers = receivers
    	self.amounts = amounts
    	self.nonce = nonce
    	self.fee = fee

    __str__(self) -> str:
        """returns a JsonString of itself"""
    	return self.string()

    __hash__(self) -> HexString:
        """returns a HexString of hash(self.__str__())"""
    	return self.hash()

    def string(self) -> str:
        """same as __str__"""
    	pass

    def hash(self) -> HexString:
        """same as __hash__"""
    	pass


def get_hashes_list(transactions: List[Transaction]) -> List[HexString]:
    """takes a list of Transaction objects and returns a list of HexString containing hash(tx) for each tx"""
	return [tx.hash() for tx in transactions]
