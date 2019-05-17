from src.chain import transaction
from src.chain.transaction import Transaction
from src.util import cryptoutil
from src.util.wallet import Wallet


def test_transaction():
    """base test for transaction"""
    sender = "iWVjc8hWuRuePAv1X8nDZdcjKcqivDUH62YKhBXBHqp2yGfgeXyHJDj5XwCHwjWB6GevCjMYT59XSBiQvMYHQ4P"
    receivers = ["01", "02", "0a"]
    amounts = [1, 2, 3]
    nonce = 1
    fee = 100
    tx = Transaction(sender, receivers, amounts, nonce, fee)

    tx_string = tx.string()
    assert tx_string == '{"sender_address": "iWVjc8hWuRuePAv1X8nDZdcjKcqivDUH62YKhBXBHqp2yGfgeXyHJDj5XwCHwjWB6GevCjMYT59XSBiQvMYHQ4P", "receivers": ["01", "02", "0a"], "amounts": [1, 2, 3], "nonce": 1, "fee": 100, "signature": ""}'
    tx_hash = tx.hash()
    assert tx_hash == "e9f65b7385ffb2e9c8809da75ff86bc10b8490dd02e3bfa26daf0c189a535b5b"


def test_unsigned_hash():
    """test the unisgned_hash of tx"""
    sender = "abcd"
    receivers = ["fe"]
    amounts = [1]
    nonce = 1
    fee = 100
    tx = Transaction(sender, receivers, amounts, nonce, fee)
    # get hashes
    tx_signed_hash = tx.hash()
    tx_unsigned_hash = tx.unsigned_hash()
    # set signature
    tx.signature = "abcd"
    # assert signed hash has changed
    assert tx.hash() != tx_signed_hash
    # assert unsigned hash has not changed
    assert tx.unsigned_hash() == tx_unsigned_hash


def test_tx_from_json():
    """test serialization and deserialization"""
    sender = "abcd"
    receivers = ["fe"]
    amounts = [1]
    nonce = 1
    fee = 100
    t1 = Transaction(sender, receivers, amounts, nonce, fee)
    t2 = transaction.from_json_string(t1.string())
    assert t1.string() == t2.string()
    assert t1.hash() == t2.hash()
    assert t1.unsigned_hash() == t2.unsigned_hash()


def test_verify_tx():
    """
    tests if a signed transaction can be validated
    we just need the address for this, because address=public_key
    """
    w = Wallet()

    sender = w.get_address()
    receivers = ["fe"]
    amounts = [1]
    nonce = 1
    fee = 100
    t = Transaction(sender, receivers, amounts, nonce, fee)
    w.sign_transaction(t)
    assert cryptoutil.verify_transaction_sig(t, t.get_signature())
