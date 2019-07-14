from neutro.src.chain import transaction
from neutro.src.chain.transaction import Transaction
from neutro.src.util.anonymous_transaction import AnonymousTransaction


def test_transaction():
    """base test for transaction"""
    sender = "iWVjc8hWuRuePAv1X8nDZdcjKcqivDUH62YKhBXBHqp2yGfgeXyHJDj5XwCHwjWB6GevCjMYT59XSBiQvMYHQ4P"
    receivers = ["01", "02", "0a"]
    amounts = [1, 2, 3]
    fee = 100
    tx = Transaction(sender, receivers, amounts, fee)
    print(tx.string())


def test_encryption_decryption_utils():
    """base test for transaction"""
    sender = "iWVjc8hWuRuePAv1X8nDZdcjKcqivDUH62YKhBXBHqp2yGfgeXyHJDj5XwCHwjWB6GevCjMYT59XSBiQvMYHQ4P"
    receivers = ["01", "02", "0a"]
    amounts = [1, 2, 3]
    fee = 100
    tx = AnonymousTransaction(sender, receivers, amounts, fee)

    message = "encrypt decrypt".encode()
    key = tx.generate_key()
    encrypted_message = tx.encrypt(key, message)
    decrypted_message = tx.decrypt(key, encrypted_message)

    assert decrypted_message == message

