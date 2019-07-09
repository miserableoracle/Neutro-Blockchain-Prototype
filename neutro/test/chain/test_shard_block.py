import pytest

import time
from neutro.src.util import stringutil
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

    assert sb.string() == '{"prev_main_hash": "1", "prev_shard_hash": "2", "height": 0, "time": 1562228422767, "miner": "3", "miner_signature": "", "miner_nonce": 0, "tx_merkle_root": "f1534392279bddbf9d43dde8701cb5be14b82f76ec6607bf8d6ad557f60f304e", "tx_count": 0}'
    assert str(sb) == sb.string()
    assert sb.hash() == "ea26e47c9b0a6625180723b8545582f462a9e1d24b02a54c50bc629308efec4b"
    assert sb.get_tx_root() == stringutil.empty_root


def test_shard_from_json():
    prev_main_hash = "1"
    prev_shard_hash = "2"
    miner = "3"
    tx_list = []

    sb = ShardBlock(prev_main_hash, prev_shard_hash, miner, tx_list)
    sb.height = 1  # make sure heigth is copied
    time.sleep(1 / 1000)  # make sure time is copied
    sb_copy = shard_block.from_json(sb.string())

    assert sb.string() == sb_copy.string()
    assert sb.hash() == sb_copy.hash()


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
