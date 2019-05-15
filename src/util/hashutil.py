"""utility for hashing"""
import hashlib


def hash_string(value: str) -> str:
    """
    Returns a fixed-length string of 64 hexadecimal characters
    """
    return hashlib.sha256(value.encode('ascii')).hexdigest()
