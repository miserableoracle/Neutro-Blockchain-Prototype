"""utility used for storing and reading wallet information on the local drive"""
from pathlib import Path

key_path = str(Path(__file__).parent.parent.parent) + "/.keys/"
Path(key_path).mkdir(parents=True, exist_ok=True)


def save(address: str, private_key, public_key):
    """saving a newly generated key pair"""
    with open("{0}/{1}.key".format(key_path, address), "w") as file:
        print("address:\n{}\npublic:\n{}\nprivate:\n{}".format(address,
                                                               public_key.exportKey(), private_key.exportKey()), file=file)


def open(address: str):
    """loading a previously generated key pair"""
    with open("{0}/{1}.key".format(key_path, address), "w") as file:
