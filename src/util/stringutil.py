"""util for working with strings"""
import json
from src.util import hashutil

# define a default hash for empty subtree roots
empty_root = hashutil.hash_string("00")


def dict_to_string(value: dict) -> str:
    """makes everythign human readable, also used for hashing stuff"""
    return json.dumps(value)


def int_to_hex_string(value: int, length: int=64) -> str:
    """returns a hex string of an int"""
    hex_string = str(hex(value))[2:]
    return "".join("0" * (length - len(hex_string))) + hex_string


def hex_string_to_int(value: str) -> int:
    """returns an int from a hex string"""
    return int(value, 16)
