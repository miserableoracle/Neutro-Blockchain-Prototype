import pytest

from src.util.wallet import Wallet
from src.util import wallet
from src.database import wallet_database


def test_generate_wallet():
    # test generating new wallet
    w = Wallet()
    # test loading wallet
    w2 = Wallet(w.get_address())
    # make sure these are the same
    assert w.get_address() == w2.get_address()
    assert w.get_public_key() == w2.get_public_key()

    # this should throw an execption
    with pytest.raises(ValueError):
        w = Wallet("ab")

    wallet_database.remove_wallet(w.get_address())


def test_wallet_sign():
    w = Wallet()

    assert w.verify(w.sign("abcde"), "abcde")
    assert wallet.verify(w.get_public_key(), w.sign("abcde"), "abcde")

    wallet_database.remove_wallet(w.get_address())
