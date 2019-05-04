"""transaction"""
from typing import Set, NewType
from util.types import Uint, Hash32
from util.addressutils import Address


class Transaction(object):

	fields = [
		(sender, Address),
		(signature, Signature),
		(receivers, List[Address]),
		(amounts, List[Uint]),
		(nonce, Uint),
		(fee, Uint)
	]
    __init__(self, sender: Address, receivers: List[Address], amounts: List[Uint], nonce: Uint, fee:uint):
    	self.sender = sender
    	self.signature = signature
    	self.receivers = receivers
    	self.amounts = amounts
    	self.nonce = nonce
    	self.fee = fee

    __str__(self):
    	return self.string()

    __hash__(self):
    	return self.hash()

    def hash(self):
    	pass

    def string(self):
    	pass


def get_hashes_list(transactions: List[Transaction]) -> List[Hash32]:
	return [tx.hash() for tx in transactions]
