from neutro.src.chain import transaction
from neutro.src.chain.transaction import Transaction
from neutro.src.util import cryptoutil
from neutro.src.util import wallet


def test_transaction():
    """base test for transaction"""
    sender = "iWVjc8hWuRuePAv1X8nDZdcjKcqivDUH62YKhBXBHqp2yGfgeXyHJDj5XwCHwjWB6GevCjMYT59XSBiQvMYHQ4P"
    receivers = ["01", "02", "0a"]
    amounts = [1, 2, 3]
    fee = 100
    tx = Transaction(sender, receivers, amounts, fee)

    assert tx.string() == \
        '{"sender": "iWVjc8hWuRuePAv1X8nDZdcjKcqivDUH62YKhBXBHqp2yGfgeXyHJDj5XwCHwjWB6GevCjMYT59XSBiQvMYHQ4P", "receivers": ["01", "02", "0a"], "amounts": [1, 2, 3], "nonce": 0, "fee": 100, "signature": ""}'
    assert tx.hash() == "a564b3a98ed7d3f66b69ee4d9f7fab588a875ae06c6f7919c7f83121bb72f859"


def test_unsigned_hash():
    """test the unisgned_hash of tx"""
    sender = "abcd"
    receivers = ["fe"]
    amounts = [1]
    fee = 100
    tx = Transaction(sender, receivers, amounts, fee)
    # get hashes
    tx_signed_hash = tx.hash()
    tx_unsigned_hash = tx.unsigned_hash()
    # no signature means equivalent hashes
    assert tx_signed_hash == tx_unsigned_hash
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
    fee = 100
    t1 = Transaction(sender, receivers, amounts, fee)
    t2 = transaction.from_json(t1.string())
    assert t1.string() == t2.string()
    assert t1.hash() == t2.hash()
    assert t1.unsigned_hash() == t2.unsigned_hash()


def test_verify_tx():
    """
    tests if a signed transaction can be validated
    we just need the address for this, because address=public_key
    """
    w = wallet.generate_new_wallet()
    sender = w.get_address()
    receivers = ["fe"]
    amounts = [1]
    fee = 100
    t = Transaction(sender, receivers, amounts, fee)
    w.sign_transaction(t)
    assert cryptoutil.verify_transaction_sig(t, t.get_signature())
    assert t.verify()


def test_unvalid_verify_tx():
    sender = "a"
    receivers = ["fe"]
    amounts = [1]
    fee = 100
    t = Transaction(sender, receivers, amounts, fee)
    assert False == t.verify()
