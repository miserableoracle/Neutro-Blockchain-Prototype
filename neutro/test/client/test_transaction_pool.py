import pytest
from neutro.src.client.transaction_pool import TransactionPool
from neutro.src.chain.transaction import Transaction
from neutro.src.chain.voting_token_transaction import VotingTokenTransaction


def test_pool():
    """test that adding the same tx twice is not possible"""
    p = TransactionPool()
    assert p.get_size() == 0
    assert p.get_tx_list() == []

    sender = "iWVjc8hWuRuePAv1X8nDZdcjKcqivDUH62YKhBXBHqp2yGfgeXyHJDj5XwCHwjWB6GevCjMYT59XSBiQvMYHQ4P"
    receivers = ["01", "02", "0a"]
    amounts = [1, 2, 3]
    fee = 100
    tx1 = Transaction(sender, receivers, amounts, fee)

    p.add(tx1)
    assert p.get_size() == 1
    assert p.get_tx_list()[0].string() == tx1.string()

    tx2 = Transaction(sender, receivers, amounts, fee)

    p.add(tx2)

    assert p.get_size() == 1
    assert p.get_tx_list()[0].string() == tx1.string()
    assert p.get_tx_list()[0].string() == tx2.string()

    p.remove(tx1)

    assert p.get_size() == 0
    assert p.get_tx_list() == []


def test_pool_multi_add_same_tx():
    p = TransactionPool()
    assert p.get_size() == 0
    assert p.get_tx_list() == []

    sender = "iWVjc8hWuRuePAv1X8nDZdcjKcqivDUH62YKhBXBHqp2yGfgeXyHJDj5XwCHwjWB6GevCjMYT59XSBiQvMYHQ4P"
    receivers = ["01", "02", "0a"]
    amounts = [1, 2, 3]
    fee = 100
    tx = Transaction(sender, receivers, amounts, fee)

    p.add(tx)

    assert p.get_size() == 1
    assert p.get_tx_list()[0].string() == tx.string()

    p.add(tx)

    assert p.get_size() == 1
    assert p.get_tx_list()[0].string() == tx.string()

    p.add(tx)

    assert p.get_size() == 1
    assert p.get_tx_list()[0].string() == tx.string()

    p.remove(tx)

    assert p.get_size() == 0
    assert p.get_tx_list() == []


def test_pool_two_different_tx():
    p = TransactionPool()

    sender = "iWVjc8hWuRuePAv1X8nDZdcjKcqivDUH62YKhBXBHqp2yGfgeXyHJDj5XwCHwjWB6GevCjMYT59XSBiQvMYHQ4P"
    receivers = ["01", "02", "0a"]
    amounts = [1, 2, 3]
    fee = 100
    tx1 = Transaction(sender, receivers, amounts, fee)
    tx1.nonce = 1
    tx2 = Transaction(sender, receivers, amounts, fee)
    tx2.nonce = 2

    p.add(tx1)
    p.add(tx2)

    assert p.get_size() == 2

    p.remove(tx2)

    assert p.get_size() == 1

    p.remove(tx2)

    assert p.get_size() == 1

    p.remove(tx1)

    assert p.get_size() == 0


def test_tx_pool_with_vtx():
    p = TransactionPool()

    sender = "0"
    receiver = "1"
    vt_amount = 1
    nto_amount = 100

    vtx = VotingTokenTransaction(sender, receiver, vt_amount, nto_amount)

    p.add(vtx)

    vtx2 = p.get_by_hash(vtx.hash())

    assert vtx == vtx2
