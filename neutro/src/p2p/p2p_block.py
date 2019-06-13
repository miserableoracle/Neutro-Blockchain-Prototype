from neutro.src.chain.block import Block


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
    block_string = b.string()
    return block_string
