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


def test_blocks():
    # test creation of blocks
    prev_hash = "0001"
    transactions = ["00af"]
    miner = "abcdef"
    difficulty = "0a"
    nonce = "000000000001"

    b = Block(prev_hash, transactions, miner,
              difficulty, nonce)
    b.time = 0
    b2 = Block(prev_hash, transactions, miner,
               difficulty, nonce)

    block_string = b.string()
    block_string2 = b2.string()
    list_blocks = []
    list_blocks.append(block_string)
    list_blocks.append(block_string2)
    return list_blocks

