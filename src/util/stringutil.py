"""util for working with strings"""
import json


def dict_to_string(value: dict):
    """makes everythign human readable, also used for hashing stuff"""
    return json.dumps(value).replace("\"", "").replace("'", "").replace("\\", "")
