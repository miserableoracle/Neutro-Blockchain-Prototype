"""class representing a Wallet and utils for this Wallet and Addresses"""
from src.util import loggerutil
from src.util import hashutil
from src.util import stringutil
from src.util import cryptoutil
from src.database import wallet_database


class Wallet(object):
    """an address"""
    fields = [
        ("address", str)
    ]

    def __init__(self, address: str = None):
        """
        either generates a new wallet and saves it
        or takes an address and opens the wallet file for this address
        """
        if not address:
            self.private_key = cryptoutil.generate_key()
            self.public_key = self.private_key.get_verifying_key()
            self.address = cryptoutil.key_to_address(self.public_key)
            self.nonce = 0
            # save the new wallet
            self.save()
        else:
            # open existing wallet
            if not isinstance(address, str):
                loggerutil.debug("could not open wallet with " +
                                 str(address) + " as address")
                raise ValueError("address needs to be string")
            self.address = address
            self.public_key = cryptoutil.address_to_key(address)
            self.private_key, self.nonce = wallet_database.open_wallet(
                self.address)

    def __str__(self) -> str:
        """returns a JsonString of itself"""
        return self.string()

    def string(self) -> str:
        """returns a JsonString of itself"""
        ret = {}
        for f in self.fields:
            ret.update({f[0]: getattr(self, f[0])})
        return stringutil.dict_to_string(ret)

    def get_address(self) -> str:
        return self.address

    def get_nonce(self) -> int:
        return self.nonce

    def get_public_key(self):
        return self.public_key

    def get_private_key(self):
        return self.private_key

    def sign_transaction(self, transaction):
        """
        signes the transaction with this wallet. Also updating the nonce.
        """
        if transaction.get_sender_address() != self.get_address():
            raise ValueError(
                "cannot sign transaction where tx.sender is different to this wallets address")
            loggerutil.info("could not sign transaction " +
                            transaction.string() + " with wallet " + self.string())
        transaction.nonce = self.nonce
        # update and save nonce
        self.nonce += 1
        # TODO: this should be optimized to just save the nonce and not the
        # whole wallet again.
        self.save()
        # set tx signature
        transaction.signature = cryptoutil.get_transaction_sig(
            self.get_private_key(), transaction)

    def save(self):
        """saves this wallet to local files"""
        wallet_database.save_wallet(self.address, self.private_key, self.nonce)
