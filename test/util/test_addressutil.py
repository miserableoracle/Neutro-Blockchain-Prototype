from src.util.addressutil import Wallet
from src.util.types import HexString
from src.util import hashutil

address = HexString("0x0123456789abcdef")
wallte = Wallet(address)
assert wallte.get_private_key() == address
assert wallet.hash() == hashutil.hash(wallet.string())
assert wallet.hash() == hashutil.hash(wallet.get_public_key())
