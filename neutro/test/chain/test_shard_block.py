import pytest

from neutro.src.chain.transaction import Transaction
from neutro.src.chain import shard_block
from neutro.src.chain.shard_block import ShardBlock


def test_shard_block():
    prev_main_hash = "1"
    prev_shard_hash = "2"
    miner = "3"
    tx_list = []

    sb = ShardBlock(prev_main_hash, prev_shard_hash, miner, tx_list)
    # time is automatically set, so we need to change it for the test
    sb.time = 1562228422767

    assert sb.string() == '{"prev_main_hash": "1", "prev_shard_hash": "2", "height": 0, "time": 1562228422767, "miner": "3", "tx_merkle_root": "f1534392279bddbf9d43dde8701cb5be14b82f76ec6607bf8d6ad557f60f304e", "tx_count": 0}'
    assert sb.hash() == "ba78db9a947358aa5a2f2fe9b8e90102982b7e28c9d58a856a88748b49a1325d"


def test_shard_from_json():
    prev_main_hash = "1"
    prev_shard_hash = "2"
    miner = "3"
    tx_list = []

    sb = ShardBlock(prev_main_hash, prev_shard_hash, miner, tx_list)
    sb_copy = shard_block.from_json(sb.string())

    assert sb.prev_main_hash == sb_copy.prev_main_hash
    assert sb.prev_shard_hash == sb_copy.prev_shard_hash
    assert sb.miner == sb.miner


def test_shard_from_json_with_tx_list():
    def get_tx_list(_range):
        return [Transaction("a" + str(i), ["b" + str(i)], [i], 10 * i) for i in range(_range)]

    prev_main_hash = "1"
    prev_shard_hash = "2"
    miner = "3"
    tx_list = get_tx_list(100)

    sb = ShardBlock(prev_main_hash, prev_shard_hash, miner, tx_list)
    # string(True) creates a string with all tx
    sb_copy = shard_block.from_json(sb.string(True))

    for i in range(100):
        tx = sb.tx_list[i]
        tx_copy = sb_copy.tx_list[i]
        assert tx.hash() == tx_copy.hash()
