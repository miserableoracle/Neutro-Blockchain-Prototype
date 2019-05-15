from src.chain.block import Block


def test_block():
    prev_hash = "0001"
    tx_merkle_root = "00af"
    miner = "abcdef"
    difficulty = "0a"
    nonce = "000000000001"
    tx_count = 10

    block = Block(prev_hash, tx_merkle_root, miner,
                  difficulty, nonce, tx_count)

    block_str = block.string()
    assert block_str == "{prev_hash: 0001, tx_merkle_root: 00af, miner: abcdef, difficulty: 0a, reward: 00, nonce: 000000000001, tx_count: 10}"
    block_hash = block.hash()
    assert block_hash == "45ec4beabf464042644164e63de3d15f57629216ae16624040609e4eeb89453a"
