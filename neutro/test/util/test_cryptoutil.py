import pytest

from neutro.src.util import cryptoutil
from neutro.src.chain.transaction import Transaction


def test_key_to_address_to_key():
    """test if key_to_address and the other way works"""
    private_key = cryptoutil.generate_key()
    public_key = private_key.get_verifying_key()
    assert public_key.to_string() == cryptoutil.address_to_key(
        cryptoutil.key_to_address(public_key)).to_string()


def test_sign_verify_message():
    """test that signing and verifying a message works"""
    message = "test"
    private_key = cryptoutil.generate_key()
    public_key = private_key.get_verifying_key()

    signature = cryptoutil.sign_message(private_key, message)
    assert cryptoutil.verify_message(public_key, message, signature)


def test_sign_transaction():
    """test that signing and verifying transaction works"""
    private_key = cryptoutil.generate_key()
    sender = cryptoutil.key_to_address(private_key.get_verifying_key())
    receivers = ["fe"]
    amounts = [1]
    fee = 100
    tx = Transaction(sender, receivers, amounts, fee)

    # get the signature
    tx_sig = cryptoutil.get_transaction_sig(private_key, tx)
    # validate transaction
    assert cryptoutil.verify_transaction_sig(tx, tx_sig)
