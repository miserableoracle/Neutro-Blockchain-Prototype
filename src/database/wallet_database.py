"""utility used for storing and reading wallet information on the local drive"""
import os
import shutil
import ecdsa
from pathlib import Path


def save_wallet(address: str, private_key: ecdsa.SigningKey, nonce: int):
    """saving a newly generated key pair"""
    key_path = str(Path(__file__).parent.parent.parent) + "/.keys/" + address
    Path(key_path).mkdir(parents=True, exist_ok=True)
    # save private key as bytes
    with open("{0}/private".format(key_path), "wb") as private_file:
        private_file.write(private_key.to_der())
    # save address (b58 encoded)
    with open("{0}/address".format(key_path), "w") as address_file:
        print("{}".format(address), file=address_file)
    # save nonce
    with open("{0}/nonce".format(key_path), "w") as nonce_file:
        print("{}".format(nonce), file=nonce_file)


def open_wallet(address: str):
    """loading a previously generated wallet"""
    key_path = str(Path(__file__).parent.parent.parent) + "/.keys/" + address
    if not os.path.isdir(key_path):
        raise ValueError("there is no wallet for address " +
                         address + " in local database")
    # read private key
    with open("{0}/private".format(key_path), "rb") as private_file:
        private_key = private_file.read()
        private_key = ecdsa.SigningKey.from_der(private_key)
    # read nonce as string
    with open("{0}/nonce".format(key_path), "r") as nonce_file:
        nonce = int(nonce_file.read())

    return private_key, nonce


def remove_wallet(address: str):
    """removes a localy saved wallet"""
    key_path = str(Path(__file__).parent.parent.parent) + "/.keys/" + address
    shutil.rmtree(key_path)
