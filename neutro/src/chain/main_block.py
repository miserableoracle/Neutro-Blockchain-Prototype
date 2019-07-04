"""class representing a block"""
import time
import json
from typing import List
from neutro.src.util import loggerutil
from neutro.src.util import hashutil
from neutro.src.util import stringutil
from neutro.src.trie.trie import Trie
from neutro.src.chain.vote import Vote
from neutro.src.chain.shard_block import ShardBlock
from neutro.src.chain.voting_token_transaction import VotingTokenTransaction
from neutro.src.database import block_database


class MainBlock(object):
    """class representing a block"""
    fields = [
        ("prev_hash", str),
        ("height", int),
        ("time", int),
        ("miner", str),
        ("difficulty", str),
        ("reward", str),
        ("nonce", str),

        ("vote_merkle_root", str),
        ("vote_list", List[Vote]),
        ("vote_count", int),

        ("shard_merkle_root", str),
        ("shard_list", List[ShardBlock]),
        ("shard_count", str),

        ("vtx_merkle_root", str),
        ("vtx_list", List[VotingTokenTransaction]),
        ("vtx_count", int),

        ("next_shard_producers", List[str])
    ]

    def __init__(self, prev_hash: str, miner: str, difficulty: str, vote_list: List[Vote], shard_list: List[ShardBlock], vtx_list=List[VotingTokenTransaction]):
        self.prev_hash = prev_hash
        self.height = 0  # TODO
        self.miner = miner
        self.time = int(time.time() * 1000)
        self.difficulty = difficulty

        if not vote_list or len(vote_list) == 0:
            self.vote_list = []
        else:
            self.vote_list = vote_list
        self.vote_trie = Trie([v.hash() for v in self.vote_list])
        self.vote_count = self.vote_trie.size()
        self.vote_merkle_root = self.vote_trie.root()

        if not shard_list or len(shard_list) == 0:
            self.shard_list = []
        else:
            self.shard_list = vote_list
        self.shard_trie = Trie([s.hash() for s in self.shard_list])
        self.shard_count = self.shard_trie.size()
        self.shard_merkle_root = self.shard_trie.root()

        if not vtx_list or len(vtx_list) == 0:
            self.vtx_list = []
        else:
            self.vtx_list = vtx_list
        self.vtx_trie = Trie([vtx.hash() for vtx in self.vtx_list])
        self.vtx_count = self.vtx_trie.size()
        self.vtx_merkle_root = self.vtx_trie.root()

        loggerutil.debug("created MainBlock: " + self.string())

    def __str__(self) -> str:
        """returns a json-string of itself excluding all lists"""
        return self.string()

    def __hash__(self) -> int:
        """returns an int as hash of this object"""
        return int(self.hash(), 16)

    def string(self, with_vote_list=False, with_shard_list=False, with_vtx_list=False) -> str:
        """
        returns a json-string of itself

        with_x_list is there to store and broadcast a 
        main-block containing all information
        """
        ret = {}
        for f in self.fields:
            ret.update({f[0]: getattr(self, f[0])})
        if not with_vote_list:
            ret.pop("vote_list")
        if not with_shard_list:
            ret.pop("shard_list")
        if not with_vtx_list:
            ret.pop("vtx_list")
        return stringutil.dict_to_string(ret)

    def hash(self) -> str:
        """returns a hex string of the hash of this object"""
        return hashutil.hash_string(self.string())


def from_json_string(json_block: str) -> MainBlock:
    """generates a block-object from a json-string"""
    _dict = json.loads(json_block)
    block = MainBlock(
        prev_hash=_dict["prev_hash"],
        miner=_dict["miner"],
        difficulty=_dict["difficulty"],
        vote_list=_dict["vote_list"],
        shard_list=_dict["shard_list"],
        vtx_list=_dict["vtx_list"]
    )
    for f in block.fields:
        block.f = _dict[f[0]]
    return block
