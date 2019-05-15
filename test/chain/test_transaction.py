from src.chain.transaction import Transaction


def test_transaction():
    sender = None
    receivers = ["01", "02", "0a"]
    amounts = [1, 2, 3]
    nonce = 1
    fee = 100

    tx = Transaction(sender, receivers, amounts, nonce, fee)

    tx_string = tx.string()
    assert tx_string == "{sender: null, receivers: [01, 02, 0a], amounts: [1, 2, 3], nonce: 1, fee: 100, v: 0, r: 0, s: 0}"
    tx_hash = tx.hash()
    assert tx_hash == "90455b22739861c633e03ef56109f6d8dc7b36df08f13915455d73a49159d854"
