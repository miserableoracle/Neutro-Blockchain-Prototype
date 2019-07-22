import pytest
from neutro.src.client.block_pool import BlockPool
from neutro.src.chain.main_block import MainBlock
from neutro.src.chain.shard_block import ShardBlock


def test_pool():
    p = BlockPool()

    assert p.get_current_height() == 0
    assert not p.get_block_dict()

    mb = MainBlock("0", "1", "2", [], [], [])

    p.add(mb)

    assert p.get_block_dict()[mb.height][0] == mb


def test_current_height():
    p = BlockPool()
    mb1 = MainBlock("0", "1", "2", [], [], [])
    mb2 = MainBlock("3", "4", "5", [], [], [])
    mb1.height = 100
    mb2.height = 101

    p.add(mb1)

    assert p.get_current_height() == 100

    p.add(mb2)

    assert p.get_current_height() == 101


def test_add_and_remove_fork_block():
    height = 100
    p = BlockPool()
    mb1 = MainBlock("0", "1", "2", [], [], [])
    mb2 = MainBlock("3", "4", "5", [], [], [])
    mb1.height = height
    mb2.height = height

    p.add(mb1)
    p.add(mb2)

    assert p.get_block_dict()[height] == [mb1, mb2]

    p.remove(mb1)

    assert p.get_block_dict()[height] == [mb2]


def test_remove_non_existing_block():
    p = BlockPool()
    mb1 = MainBlock("0", "1", "2", [], [], [])

    with pytest.raises(ValueError):
        p.remove(mb1)

    mb2 = MainBlock("3", "4", "5", [], [], [])
    p.add(mb2)

    with pytest.raises(ValueError):
        p.remove(mb1)


def test_with_shard_block():
    p = BlockPool()
    sb1 = ShardBlock("0", "1", "2", [])
    sb1.height = 50000

    p.add(sb1)

    assert p.get_blocks_by_height(50000) == [sb1]

    p.remove(sb1)

    assert not p.get_blocks_by_height(50000)
    assert not p.get_block_dict()
