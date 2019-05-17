"""util for working with strings"""
import json
from src.util import hashutil

# define a default hash for empty subtree roots
empty_root = hashutil.hash_string("00")


def dict_to_string(value: dict):
    """makes everythign human readable, also used for hashing stuff"""
    return json.dumps(value)
