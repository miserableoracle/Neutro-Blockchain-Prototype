from src.chain.transaction import Transaction

sender = Wallet(HexString("0x0123456789abcdef")).string()
receivers = [Wallet(HexString("0x0123456789abcdee")).string(),
             Wallet(HexString("0x0123456789abcded")).string()]
amounts = [HexString("0x01"), HexString("0x02")]
nonce = HexString("0x00")
fee = HexString("0x0f")

tx = Transaction(sender, receivers, amounts, nonce, fee)
# todo calc hash and sig manualy and assert ==
