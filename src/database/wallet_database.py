"""utility used for storing and reading wallet information on the local drive"""
import os
import shutil
import ecdsa
from pathlib import Path

from src.util import loggerutil


def save_wallet(address: str, private_key: ecdsa.SigningKey, nonce: int):
    """saving a newly generated key pair"""
    wallet_path = str(Path(__file__).parent.parent.parent) + \
        "/.data/wallet/" + address
    Path(wallet_path).mkdir(parents=True, exist_ok=True)
    # save private key as bytes
    with open("{0}/private".format(wallet_path), "wb") as private_file:
        private_file.write(private_key.to_der())
    # save address (b58 encoded)
    with open("{0}/address".format(wallet_path), "w") as address_file:
        print("{}".format(address), file=address_file)
    # save nonce
    with open("{0}/nonce".format(wallet_path), "w") as nonce_file:
        print("{}".format(nonce), file=nonce_file)


def open_wallet(address: str):
    """loading a previously generated wallet"""
    wallet_path = str(Path(__file__).parent.parent.parent) + \
        "/.data/wallet/" + address
    if not os.path.isdir(wallet_path):
        loggerutil.error("could not load wallet for address " + address)
        raise ValueError("there is no wallet for address " +
                         address + " in local database")
    # read private key
    with open("{0}/private".format(wallet_path), "rb") as private_file:
        private_key = private_file.read()
        private_key = ecdsa.SigningKey.from_der(private_key)
    # read nonce as string
    with open("{0}/nonce".format(wallet_path), "r") as nonce_file:
        nonce = int(nonce_file.read())

    return private_key, nonce


def remove_wallet(address: str):
    """
    removes a localy saved wallet, this is just for testing purpouses
    WARNING: use with care, it will delete your private key with no way to get it back!!
    """
    wallet_path = str(Path(__file__).parent.parent.parent) + \
        "/.data/wallet/" + address
    shutil.rmtree(wallet_path)
