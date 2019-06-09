"""utility used for storing and reading wallet information on the local drive"""
import os
import shutil
import ecdsa
from pathlib import Path

from neutro.src.util import loggerutil
from neutro.src.util.wallet import Wallet


def save_wallet(wallet: Wallet):
    """saves a wallet"""
    wallet_path = str(Path(__file__).parent.parent.parent) + "/.data/wallet/"
    Path(wallet_path).mkdir(parents=True, exist_ok=True)
    # save private key as bytes
    with open("{0}/private".format(wallet_path), "wb") as private_file:
        private_file.write(wallet.get_private_key().to_der())
    # save address (b58 encoded)
    with open("{0}/address".format(wallet_path), "w") as address_file:
        print("{}".format(wallet.get_address()), file=address_file)
    # save nonce
    with open("{0}/nonce".format(wallet_path), "w") as nonce_file:
        print("{}".format(wallet.get_nonce()), file=nonce_file)


def load_wallet() -> Wallet:
    """opens the locally saved wallet"""
    wallet_path = str(Path(__file__).parent.parent.parent) + "/.data/wallet/"
    if not os.path.isdir(wallet_path):
        msg = "cannot open non existing wallet, try generating a wallet first"
        loggerutil.error(msg)
        raise ValueError(msg)
    # read private key
    with open("{0}/private".format(wallet_path), "rb") as private_file:
        private_key = private_file.read()
        private_key = ecdsa.SigningKey.from_der(private_key)
    # read nonce as string
    with open("{0}/nonce".format(wallet_path), "r") as nonce_file:
        nonce = int(nonce_file.read())
    # generate the wallet
    return Wallet(private_key, nonce)


def save_nonce(nonce: int):
    """saves the nonce"""
    wallet_path = str(Path(__file__).parent.parent.parent) + "/.data/wallet/"
    if not os.path.isdir(wallet_path):
        msg = "cannot save nonce to non existing wallet, try generating a wallet first"
        loggerutil.error(msg)
        raise ValueError(msg)
    # save nonce
    with open("{0}/nonce".format(wallet_path), "w") as nonce_file:
        print("{}".format(wallet.get_nonce()), file=nonce_file)


def get_nonce() -> int:
    """opens a wallet and returns the nonce"""
    return load_wallet().get_nonce()


def get_address() -> str:
    """opens a wallet and returns the address"""
    return load_wallet().get_address()
