import pytest

import time
from neutro.src.util import stringutil
from neutro.src.chain import block
from neutro.src.chain.block import Block
from neutro.src.consensus.base_pow import Pow


def test_pow_easy():
    # test pow with easy difficulty
    prev_hash = "0"
    transactions = ["00af"]
    miner = "abcdef"
    difficulty = "00ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    nonce = "0000000000000000"
    b = Block(prev_hash, transactions, miner,
              difficulty, nonce)
    p = Pow(b)
    p.start()
    p.join()
    block = p.get_mined_block()
    assert block.hash().startswith("00")


def test_pow_hard():
    # test pow with hard difficulty
    prev_hash = "0"
    transactions = ["00af"]
    miner = "abcdef"
    difficulty = "0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    nonce = "0000000000000000"
    b = Block(prev_hash, transactions, miner,
              difficulty, nonce)
    p = Pow(b)
    p.start()
    p.join()
    block = p.get_mined_block()
    assert block.hash().startswith("0000")


def test_pow_interrupt():
    # test pow with hard difficulty and interrupt the thread
    prev_hash = "0"
    transactions = ["00af"]
    miner = "abcdef"
    difficulty = "00000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    nonce = "0000000000000000"
    b = Block(prev_hash, transactions, miner,
              difficulty, nonce)
    p = Pow(b)
    p.start()

    with pytest.raises(Exception):
        p.get_mined_block()

    # assert that the thread is still running
    assert p.isAlive()
    assert not p.isInterrupted()

    # stop  the thread and expect a warning that mining was not finished
    with pytest.raises(Exception):
        p.interrupt()

    assert p.isInterrupted()
    # w8 100 ms (10 should be sufficciant, but we want to be sure)
    # for the thread to stop (should be enough)
    # normally one would use p.join(), but the test ensures that it dosent
    # take ages to interrupt the mining
    time.sleep(100 / 1000)
    assert not p.isAlive()
