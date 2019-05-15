from src.chain.block import Block
from src.chain import block


def test_block():
    # test creation of blocks
    prev_hash = "0001"
    transactions = ["00af"]
    miner = "abcdef"
    difficulty = "0a"
    nonce = "000000000001"

    b = Block(prev_hash, transactions, miner,
              difficulty, nonce)

    block_hash = b.hash()
    assert block_hash == "077e083970f9200d378c52caca06d7171238b7fb7dcf13f1e3d2364daba83ce2"


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
