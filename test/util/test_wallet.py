import pytest

from src.util.wallet import Wallet
from src.util import wallet
from src.database import wallet_database
from src.chain.transaction import Transaction


def test_generate_wallet():
    # test generating new wallet
    w1 = Wallet()
    # test loading wallet
    w2 = Wallet(w1.get_address())
    # make sure these are the same
    assert w1.get_address() == w2.get_address()
    assert w1.get_public_key() == w2.get_public_key()

    # remove the wallet
    wallet_database.remove_wallet(w1.get_address())

    # this should throw an execption
    with pytest.raises(ValueError):
        w3 = Wallet(w1.get_address())


def test_wallet_sign():
    w = Wallet()
    # verify and sign a message with wallet
    assert w.verify(w.sign("abcde"), "abcde")
    assert wallet.verify(w.get_public_key(), w.sign("abcde"), "abcde")

    wallet_database.remove_wallet(w.get_address())


def test_sign_transaction():
    # test if transactions can be signed
    w = Wallet()
    t = Transaction(sender=None, receivers=[
        "01"], amounts=[1], nonce=1, fee=100)

    public_key = w.get_public_key()
    signature = w.sign(t.hash())

    assert wallet.verify(public_key, signature, t.hash())

    wallet_database.remove_wallet(w.get_address())
