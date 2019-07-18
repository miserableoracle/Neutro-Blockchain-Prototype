import time
from neutro.src.client.client_runner import State
from neutro.src.client.client_runner import Client
from neutro.src.client.block_pool import BlockPool

"""
def get_vote_list(_range):
    return [Vote("a" + str(i), "b" + str(i), "sig" + str(i)) for i in range(_range)]


def get_shard_list(_range):
    def get_tx_list(tx_range):
        return [Transaction("a" + str(i), ["b" + str(i)], [i], 10 * i) for i in range(_range)]
    return [ShardBlock("a" + str(i), "b" + str(i), "c" + str(i), get_tx_list(10)) for i in range(_range)]


def get_vtx_list(_range):
    return [VotingTokenTransaction("a" + str(i), "b" + str(i), i, i) for i in range(_range)]

"""


def get_main_block_pool():
    """creates a dummy chain in a pool"""
    pool = BlockPool()
    prev_hash = "0"
    for i in range(100):
        b = MainBlock(prev_hash, "miner" +
                      str(i), "difficulty", [], [], [])
        b.height = i
        prev_hash = b.hash()
        pool.add_block(b)
    return pool


def test_update_chain():
    # start the client that acts as network
    c1 = Client()
    # set the main_block_pool
    c1.main_block_pool = get_main_block_pool()
    c1.height = 99
    c1.start()

    # create client 2
    c2 = Client()
    # connect to c1
    c2.connect(c1.peer.endpoint)
    # start c2, this should update_chain c2
    c2.height = 0
    c2.start()

    # w8 for 10 secs
    time.sleep(10)

    assert c1.current_height == 99
    assert c1.current_height == c2.current_height

    c1.stop()
    c2.stop()


def test_update_metadata():
    c1 = Client()
    c1.difficulty = "0"
    c1.start()
    # w8 for the client 1 to start up
    while c1.state == State.UPDATING:
        pass

    c2 = Client()
    c2.connect(c1)
    c2.start()
    # w8 for the client 2 to start up
    while c2.state == State.UPDATING:
        pass

    assert c1.difficulty == c2.difficulty
    assert c1.current_height == c2.current_height
    assert c1.stable_height == c2.stable_heigh

    c1.stop()
    c2.stop()


def test_client_state_transition_and_shard_generation()
    c1 = Client()
    p1 = Peer()

    c1.connect(p1)
    c1.start()

    m = MainBlock("prev_hash", "miner", "difficulty", [], [], [])
    m.next_shard_producers = ["address1", "address2",
                              c1.wallet.get_address(), "address4", "address5", "address6"]
    m.height = 0
    p1.send_main_block(m)

    while c1.state == State.UPDATING:
        pass
    assert c1.state == State.WAITING

    sb1 = ShardBlock(m.hash(), "0", "address1", [])
    p1.send_shard_block(sb1)

    time.sleep(100 / 1000)
    assert c1.shard_block_pool.contains(sb1)
    assert c1.state == State.WAITING

    sb2 = ShardBlock(m.hash(), sb1.hash(), "address2", [])
    sb2.height = 1
    p1.send_shard_block(sb2)

    time.sleep(100 / 1000)
    assert c1.shard_block_pool.contains(sb1)
    assert c1.shard_block_pool.contains(sb2)

    # etc. would be nice to test like this

    # assert that shard 3 is from c1
    c1.stop()


def test_update_chain_with_forks()
    c1
    c2

    c3.connect(c1.peer.endpoint)
    c3.connect(c2.peer.endpoint)

    assert c1.height == c3.height
    assert c2.height == c3.height
