from src.chain.transaction import Transaction


def test_transaction():
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
    sender = "iWVjc8hWuRuePAv1X8nDZdcjKcqivDUH62YKhBXBHqp2yGfgeXyHJDj5XwCHwjWB6GevCjMYT59XSBiQvMYHQ4P"
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
    # assert signed hash
    assert tx.hash() != tx_signed_hash
    # assert unsigned hash
    assert tx.unsigned_hash() == tx_unsigned_hash


def test_tx_from_json():
