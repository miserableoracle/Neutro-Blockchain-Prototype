from src.chain.transaction import Transaction


def test_transaction():
    sender = "0ce4649d4ac9a1f2a231362e90376076bd0bed2294afcc968550a07109c3b02d"
    receivers = ["01", "02", "0a"]
    amounts = [1, 2, 3]
    nonce = 1
    fee = 100

    tx = Transaction(sender, receivers, amounts, nonce, fee)

    tx_string = tx.string()
    assert tx_string == '{"sender_address": "0ce4649d4ac9a1f2a231362e90376076bd0bed2294afcc968550a07109c3b02d", "receivers": ["01", "02", "0a"], "amounts": [1, 2, 3], "nonce": 1, "fee": 100, "signature": ""}'
    tx_hash = tx.hash()
    assert tx_hash == "c37414cdd1214fa3ffa65e8fb973578ac641b182a84f99534e050c0bc22bc0e7"


def test_unsigned_hash():
    sender = "077e083970f9200d378c52caca06d7171238b7fb7dcf13f1e3d2364daba83ce2"
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
