from src.chain.transaction import Transaction

sender = None
receivers = ["0x01", "0x02"]
amounts = [1, 2]
nonce = 1
fee = 100

tx = Transaction(sender, receivers, amounts, nonce, fee)

tx_string = tx.string()
assert tx_string == '{"sender": null, "receivers": ["0x01", "0x02"], "amounts": [1, 2], "nonce": 1, "fee": 100, "v": 0, "r": 0, "s": 0}'
tx_hash = tx.hash()
assert tx_hash == '9ce1e441761e875186d496c6be941035cd8c620e906238f55936d5f51165b1e8'
