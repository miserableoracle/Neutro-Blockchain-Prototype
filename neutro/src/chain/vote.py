"""
this class represents a vote that can be broadcasted to the network

the yellow paper of neutro states that peers get voting rights according to the amount of voting_tokens they posess
"""
import json
import copy
from neutro.src.util import stringutil
from neutro.src.util import hashutil


class Vote(object):
    """
    a vote consists of
            - previous_block_hash
            - random nonce
            - signature of the sender of the vote
    """

    fields = [
        ("prev_hash", str),
        ("sender", str),
        ("nonce", str),
        ("signature", str)
    ]

    def __init__(self, prev_hash: str, sender: str, nonce: str, signature: str=""):
        self.prev_hash = prev_hash
        self.sender = sender
        self.nonce = nonce
        self.signature = signature

    def __str__(self) -> str:
        """returns a JsonString of itself"""
        return self.string()

    def __hash__(self) -> int:
        """returns an int as hash of this object"""
        return int(self.hash(), 16)

    def string(self) -> str:
        """same as __str__"""
        ret = {}
        for f in self.fields:
            ret.update({f[0]: getattr(self, f[0])})
        return stringutil.dict_to_string(ret)

    def hash(self) -> str:
        """not the same as __hash__"""
        return hashutil.hash_string(self.string())

    def unsigned_hash(self) -> str:
        """creates an unsigned vote and returns a hash of it"""
        v = copy.copy(self)
        v.signature = ""
        return v.hash()

    def get_sender_address(self) -> str:
        """returns the sender of this vote"""
        return self.sender


def from_json_string(json_string: str) -> Vote:
    """generates a vote-object from a json-string"""
    _dict = json.loads(json_string)
    v = Vote(
        prev_hash=_dict["prev_hash"],
        sender=_dict["sender"],
        nonce=_dict["nonce"],
        signature=_dict["signature"]
    )
    return v
