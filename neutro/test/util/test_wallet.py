import pytest

from neutro.src.util.wallet import Wallet
from neutro.src.util import wallet
from neutro.src.database import wallet_database
from neutro.src.chain.transaction import Transaction


def test_generate_wallet():
    # test generating new wallet
    w = wallet.generate_new_wallet()
    assert w is not None
    assert w.get_address() is not None
    assert w.get_nonce() == 0


def test_sign_transaction():
    # test if transactions can be signed
    w = wallet.generate_new_wallet()
    t = Transaction(sender=w.get_address(), receivers=[
        "01"], amounts=[1], fee=100)
    w.sign_transaction(t)
    assert t.verify()


def test_sign_unvalid_tx():
    # test if signing unvalid transaction is rejected
    w = wallet.generate_new_wallet()
    t = Transaction(sender="different sender than wallet", receivers=[
        "01"], amounts=[1], fee=100)
    with pytest.raises(ValueError):
        w.sign_transaction(t)


def test_nonce_correctly():
    # test if the nonce increases when signing a tx
    # test if loaded wallet (w_copy) has correct nonce
    w = wallet.generate_new_wallet()
    t = Transaction(sender=w.get_address(), receivers=[
        "01"], amounts=[1], fee=100)
    assert w.get_nonce() == 0
    w.sign_transaction(t)
    assert w.get_nonce() == 1


def test_nonce_in_tx_correct():
    # test if the nonce is correct in the tx
    w = wallet.generate_new_wallet()

    t = Transaction(sender=w.get_address(), receivers=[
        "01"], amounts=[1], fee=100)

    tx_hash_old = ""
    tx_sig_old = ""
    for i in range(10):
        # sign tx
        w.sign_transaction(t)
        # get sig
        signature = t.get_signature()
        # nonce gets bigger every signed tx
        assert t.nonce == w.get_nonce() - 1
        assert t.nonce == i
        # make sure tx_signature changes
        assert signature != tx_sig_old
        # make sure tx_hash changes
        assert t.hash() != tx_hash_old
        # finally test if verify works
        assert t.verify()
        # save values for next iteration
        tx_hash_old = t.hash()
        tx_sig_old = signature
    # assert that we counted correctly
    assert w.get_nonce() == 10
