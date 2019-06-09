import pytest

from neutro.src.util import wallet
from neutro.src.database import wallet_database


def test_save_load_wallet():
    # saving and loading wallet
    w1 = wallet.generate_new_wallet()
    wallet_database.save_wallet(w1)
    w2 = wallet_database.load_wallet()
    assert w1.get_address() == w2.get_address()
    assert w1.get_private_key().to_der() == w2.get_private_key().to_der()
    assert w1.get_nonce() == w2.get_nonce()


def test_get_address():
    w = wallet.generate_new_wallet()
    wallet_database.save_wallet(w)
    assert w.get_address() == wallet_database.get_address()


def test_get_nonce():
    w = wallet.generate_new_wallet()
    wallet_database.save_wallet(w)
    assert w.get_nonce() == wallet_database.get_nonce()


def test_save_nonce():
    w = wallet.generate_new_wallet()
    wallet_database.save_wallet(w)
    assert wallet_database.load_wallet().get_nonce() == 0
    wallet_database.save_nonce(10)
    assert wallet_database.load_wallet().get_nonce() == 10
    assert wallet_database.get_nonce() == 10
