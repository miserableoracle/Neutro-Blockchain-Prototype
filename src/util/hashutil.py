"""utility for hashing"""
import hashlib
import json


def hash_block(block: dict) -> str:
    """
    Creates a SHA-256 hash of a Block
    """

    # Order the dictionary
    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()


def hash_string(value: str) -> str:
    """
    Returns a fixed-length string of 64 hexadecimal characters
    """
    return hashlib.sha256(value.encode('ascii')).hexdigest()


