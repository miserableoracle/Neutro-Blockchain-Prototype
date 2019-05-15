import logging
from src.chain.transaction import Transaction

sender = None
receivers = ["0x01", "0x02"]
amounts = [1, 2]
nonce = 1
fee = 100

tx = Transaction(sender, receivers, amounts, nonce, fee)
# todo calc hash and sig manualy and assert ==

logging.getLogger().debug(tx.string())
