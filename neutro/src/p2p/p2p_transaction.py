#from neutro.src.chain import transaction
from neutro.src.chain.transaction import Transaction


def test_transaction():
    """base test for transaction"""
    sender = "iWVjc8hWuRuePAv1X8nDZdcjKcqivDUH62YKhBXBHqp2yGfgeXyHJDj5XwCHwjWB6GevCjMYT59XSBiQvMYHQ4P"
    receivers = ["01", "02", "0a"]
    amounts = [1, 2, 3]
    nonce = 1
    fee = 100
    tx = Transaction(sender, receivers, amounts, nonce, fee)

    tx_string = tx.string()
    return tx_string


def send_transaction(tx_string: str):
    return tx_string

