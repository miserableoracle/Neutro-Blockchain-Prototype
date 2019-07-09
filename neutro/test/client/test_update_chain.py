#from neutro.src.client.client_runner import Client
from neutro.src.client.client_runner import Client
from neutro.src.p2p.p2p_api import P2P_API
from neutro.src.database import peer_block_database
from neutro.src.chain import block
from neutro.src.chain.block import Block
from neutro.src.util import loggerutil
import pytest
import time


def save_multiple_blocks(client):
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
        print("reset the db after tests!")
        #peer_block_database.remove_database()


def client_one():
    print("client 1")
    p2p_api = P2P_API()
    peer = p2p_api.create_a_peer(role="core1", name="core1", host=("127.0.0.1", 8000))
    client_1 = Client(peer)
    save_multiple_blocks(client_1)
    save_multiple_blocks(client_1)
    save_multiple_blocks(client_1)
    client_1.stop.set()


def client_two():
    loggerutil.debug("client 2")
    p2p_api = P2P_API()
    peer = p2p_api.create_a_peer(role="switch1", name="switch1", host=("127.0.0.1", 8001))
    client_2 = Client(peer)
    save_multiple_blocks(client_2)
    save_multiple_blocks(client_2)
    client_2.stop.set()


def client_three():
    loggerutil.debug("client 3")
    p2p_api = P2P_API()
    peer = p2p_api.create_a_peer(role="switch3", name="switch3", host=("127.0.0.1", 8002))
    client_3 = Client(peer)
    save_multiple_blocks(client_3)
    client_3.stop.set()


def test_store_blocks_by_clients():
    client_one()
    client_two()
    client_three()
    

def test_update_chain():
    pass

