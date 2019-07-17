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


def test_update_chain_two_clients():
    # start the client that acts as network
    c1 = Client()
    # set the main_block_pool
    c1.main_block_pool = get_main_block_pool()
    c1.start()

    # create client 2
    c2 = Client()
    # connect to c1
    c2.connect(c1.peer)
    # start c2, this should update_chain c2
    c2.start()

    # w8 for 10 secs
    time.sleep(10)

    assert c1.current_height == 99
    assert c1.current_height == c2.current_height


def test_publish_new_block():
    c1 = Client()
    c1.difficulty = "0"
    c1.start()
    # w8 for the client to start up and start mining
    while c1.state == State.UPDATING:
        pass

    c2 = Client()
