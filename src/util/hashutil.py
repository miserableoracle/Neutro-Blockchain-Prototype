"""utility for hashing"""
import hashlib


def hash_string(value: str) -> str:
    """
    returns a fixed-length string of 64 hexadecimal chars
    """
    return hashlib.sha256(value.encode("ascii")).hexdigest()


def hash_bytes(value: bytes) -> str:
    """
    returns a fixed-length string of 64 hexadecimal chars
    """
    return hash_string(value.decode("utf-8"))


def hash_tuple(value1: str, value2: str) -> str:
    """
    returns a fixed-length string of 64 hexadecimal chars
    """
    return hashlib.sha256((value1 + value2).encode("ascii")).hexdigest()
