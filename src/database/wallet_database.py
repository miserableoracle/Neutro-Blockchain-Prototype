"""utility used for storing and reading wallet information on the local drive"""
from Crypto.PublicKey import RSA
from pathlib import Path
import os
import shutil


def save_wallet(address: str, private_key, public_key, nonce: int):
    """saving a newly generated key pair"""
    key_path = str(Path(__file__).parent.parent.parent) + "/.keys/" + address
    Path(key_path).mkdir(parents=True, exist_ok=True)
    with open("{0}/private".format(key_path), "w") as private_file:
        print("{}".format(private_key.exportKey(
            format="PEM").decode()), file=private_file)
    with open("{0}/public".format(key_path), "w") as public_file:
        print("{}".format(public_key.exportKey(
            format="PEM").decode()), file=public_file)
    with open("{0}/address".format(key_path), "w") as address_file:
        print("{}".format(address), file=address_file)
    with open("{0}/nonce".format(key_path), "w") as nonce_file:
        print("{}".format(nonce), file=nonce_file)


def open_wallet(address: str):
    """loading a previously generated key pair"""
    key_path = str(Path(__file__).parent.parent.parent) + "/.keys/" + address
    if not os.path.isdir(key_path):
        raise ValueError("there is no wallet for address " +
                         address + " in local database")
    with open("{0}/private".format(key_path), "rb") as private_file:
        private_key = RSA.importKey(private_file.read())
    with open("{0}/public".format(key_path), "rb") as public_file:
        public_key = RSA.importKey(public_file.read())
    with open("{0}/nonce".format(key_path), "r") as public_file:
        nonce = int(public_file.read())
    return private_key, public_key, nonce


def remove_wallet(address: str):
    """removes a localy saved wallet"""
    key_path = str(Path(__file__).parent.parent.parent) + "/.keys/" + address
    shutil.rmtree(key_path)
