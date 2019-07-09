import pytest

from neutro.src.chain import block
from neutro.src.chain.block import Block
from neutro.src.database import peer_block_database
from neutro.src.client.client_runner import Client


def test_block():
    # test creation of blocks
    prev_hash = "0001"
    transactions = ["00af"]
    miner = "abcdef"
    difficulty = "0a"
    nonce = "000000000001"

    b = Block(prev_hash, transactions, miner,
              difficulty, nonce)
    b.time = 0

    block_hash = b.hash()
    assert block_hash == "af51c2a176fdda2f5d00d4a7aa8a194a7d3bc3caa6beafd9a207727d7cdfc241"


def test_block_no_tx():
    # test block with 0 tx
    prev_hash = "0001"
    transactions = []
    miner = "abcdef"
    difficulty = "0a"
    nonce = "000000000001"

    # make 2 blocks with [] and None as txs
    b1 = Block(prev_hash, transactions, miner,
               difficulty, nonce)

    transactions = None
    b2 = Block(prev_hash, transactions, miner,
               difficulty, nonce)
    b2.time = b1.time

    assert b1.string() == b2.string()
    assert b1.hash() == b2.hash()
    assert b1.get_tx_root() == b2.get_tx_root()


def test_block_from_json():
    prev_hash = "abc"
    transactions = ["a", "b", "c", "d", "e", "f"]
    miner = "afebc001"
    difficulty = "000afx"
    nonce = "1"

    b1 = Block(prev_hash, transactions, miner,
               difficulty, nonce)
    b2 = block.from_json_string(b1.string())

    assert b1.string() == b2.string()
    assert b1.hash() == b2.hash()


def test_save_load_block():
    """save a block to local storage and read it from there"""
    prev_hash = "abc"
    transactions = ["a", "b", "c", "d", "e", "f"]
    miner = "afebc001"
    difficulty = "000afx"
    nonce = "1"
    try:
        b1 = Block(prev_hash, transactions, miner,
                   difficulty, nonce)
        b1.save()

        b2 = block.from_json_string(
            peer_block_database.load_block_by_height(b1.get_heigth()))

        b3 = block.from_json_string(
            peer_block_database.load_block_by_hash(b1.hash()))

        assert b1.hash() == b2.hash()
        assert b2.hash() == b3.hash()
    finally:
        # reset the database
        peer_block_database.remove_database()


def test_block_height():
    """tests that the height of the block is calculated correctly"""
    prev_hash = "abc"
    transactions = ["a", "b", "c", "d", "e", "f"]
    miner = "afebc001"
    difficulty = "000afx"
    nonce = "1"
    try:
        b1 = Block(prev_hash, transactions, miner,
                   difficulty, nonce)
        b1.save()
        assert b1.get_heigth() == 0
        b2 = Block(prev_hash, transactions, miner,
                   difficulty, nonce)
        assert b2.get_heigth() == 1

    finally:
        # reset the database
        peer_block_database.remove_database()


def test_save_multiple_blocks(client):
    """save multiple blocks with different height"""
    prev_hash = "abc"
    transactions = ["a", "b", "c", "d", "e", "f"]
    miner = "afebc001"
    difficulty = "000afx"
    nonce = "1"
    try:
        # save block 1
        b1 = Block(prev_hash, transactions, miner,
                   difficulty, nonce, client)
        b1.peer_save(client)
        # save block 2
        b2 = Block(prev_hash, transactions, miner,
                   difficulty, nonce, client)
        b2.peer_save(client)

        with pytest.raises(ValueError):
            b2.height = 0
            b2.peer_save(client)
    finally:
        # reset the database
        peer_block_database.remove_database()


def test_get_current_height():
    """saves multiple blocks and tests that block_database.get_current_height() is correct"""
    assert peer_block_database.get_current_height() == -1

    try:
        for i in range(10):
            prev_hash = "abc"
            transactions = ["a", "b", "c", "d", "e", "f"]
            miner = "afebc001"
            difficulty = "000afx"
            nonce = "1"
            b1 = Block(prev_hash, transactions, miner,
                       difficulty, nonce)
            b1.height = i
            b1.save()

            assert peer_block_database.get_current_height() == i
    finally:
        peer_block_database.remove_database()

