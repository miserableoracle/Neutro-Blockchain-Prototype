import pytest

import time
from neutro.src.util import stringutil
from neutro.src.chain import main_block
from neutro.src.chain import shard_block
from neutro.src.chain.main_block import MainBlock
from neutro.str.chain.vote import Vote
from neutro.src.chain.transactin import Transaction
from neutro.src.chain.shard_block import ShardBlock
from neutro.src.chain.voting_token_transaction import VotingTokenTransaction


def get_vote_list(_range):
    return [Vote("a" + str(i), "b" + str(i), [i], "sig" + str(i)) for i in range(_range)]


def get_shard_list(_range):
    def get_tx_list(tx_range):
        return [Transaction("a" + str(i), ["b" + str(i)], [i], 10 * i) for i in range(_range)]
    return [ShardBlock("a" + str(i), "b" + str(i), "c" + str(i), get_tx_list(10)) for i in range(_range)]


def get_vtx_list(_range):
    return [VotingTokenTransaction("a" + str(i), "b" + str(i), i, i) for i in range(_range)]


def test_main_block():
    prev_hash = "1"
    miner = "2"
    difficulty = "3"

    mb = MainBlock(prev_hash, miner, difficulty, [], [], [])
    # time is automatically set, so we need to change it for the test
    mb.time = 1562228422767

    assert mb.string() == '{"prev_hash": "1", "height": 0, "time": 1562228422767, "miner": "2", "difficulty": "3", "nonce": "0000000000000000", "vote_merkle_root": "f1534392279bddbf9d43dde8701cb5be14b82f76ec6607bf8d6ad557f60f304e", "vote_count": 0, "shard_merkle_root": "f1534392279bddbf9d43dde8701cb5be14b82f76ec6607bf8d6ad557f60f304e", "shard_count": 0, "vtx_merkle_root": "f1534392279bddbf9d43dde8701cb5be14b82f76ec6607bf8d6ad557f60f304e", "vtx_count": 0, "next_shard_producers": []}'
    assert str(mb) == mb.string()
    assert mb.hash() == "8becb0feaf4b853fd84b38ddf3098a14d2f08d890cb7ecbdfdbc18dff9a72bd5"
    assert mb.get_vote_root() == stringutil.empty_root
    assert mb.get_shard_root() == stringutil.empty_root
    assert mb.get_vtx_root() == stringutil.empty_root


def test_main__from_json():
    prev_hash = "1"
    miner = "2"
    difficulty = "3"

    mb = MainBlock(prev_hash, miner, difficulty, [], [], [])
    mb.height = 1  # make sure height is copied
    time.sleep(1 / 1000)  # make sure time is copied
    mb.nonce = "abcdabcdabcdabcd"  # make sure nonce is copied
    # make sure shard producers are copied
    mb.next_shard_producers = ["a", "b", "c"]
    mb_copy = main_block.from_json(mb.string())

    assert mb.string() == mb_copy.string()
    assert mb.hash() == mb_copy.hash()


def test_main_from_json_with_vote_list():
    pass


def test_main_from_json_with_shard_list():
    pass


def test_main_from_json_with_vtx_list():
    pass


def test_main_from_json_with_all_lists():
    pass
