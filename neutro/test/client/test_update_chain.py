from neutro.src.client.client_runner import Client
from neutro.src.p2p.p2p_api import P2P_API
from neutro.src.chain.main_block import MainBlock
from neutro.src.chain.transaction import Transaction
from neutro.src.database.p2p_messages_database import remove_database
import pytest
import time
import datetime as date
from neutro.src.util import loggerutil


def create_blockchain(blocks):

    def create_genesis_block():
        # manually constructs a block with height 0 and an arbitrary previous hash
        mb = MainBlock("0", "1", "3", [], [], [])
        mb.height = 0
        mb.time = 1562228422767
        return mb

    def next_block(last_block):
        # Generate all later blocks in the blockchain
        current_height = last_block.height + 1
        #current_hash = last_block.hash # ToDo: fix hash error from main_block?
        mb = MainBlock(current_height, "3", "4", [], [], [])
        mb.height = current_height
        mb.time = 1562228422767
        return mb

    # Create the blockchain and add the genesis block
    blockchain = [create_genesis_block()]

    previous_block = blockchain[0]

    print("Hash: {0}\n".format(blockchain[0].hash()))

    num_of_blocks_to_add = blocks

    # Add blocks to the chain
    for i in range(0, num_of_blocks_to_add):
        block_to_add = next_block(previous_block)
        print(block_to_add)
        blockchain.append(block_to_add)
        previous_block = block_to_add
        print("Block #{0} has been added to the blockchain!".format(
            block_to_add.height))
        print("Hash: {0}\n".format(blockchain[i].hash()))

    #print(*blockchain, sep="\n")
    return blockchain


def test_clients_send_block_broadcast():
    """ test case for broadcasting between two clients"""
    # creates a P2P_API object
    p2p_api = P2P_API()
    # creates a peer named core
    peer = p2p_api.create_a_peer(
        role='core', name='core', host=('0.0.0.0', 8000))
    dummy_peer = p2p_api.create_a_peer(
        role="sw", name="switch_1", host=("127.0.0.1", 8011))
    # creates an instance of Client with the specified peer above
    # Todo: Current __init__ doesn't have 4 positional arguments (including self), future consideration?
    client_1 = Client(create_blockchain(2), peer, dummy_peer)

    # creates a peer named switch_2 with the role sw
    peer2 = p2p_api.create_a_peer(
        role='sw', name='switch_2', host=('0.0.0.0', 8012))
    # creates a Client with the specified peer above and connect it to the peer of client 1
    client_2 = Client(create_blockchain(3), peer2, client_1.peer)
    peer3 = p2p_api.create_a_peer(
        role='sw', name='switch_3', host=('0.0.0.0', 8013))
    # creates a Client with the specified peer above and connect it to the peer of client 1
    client_3 = Client(create_blockchain(3), peer3, client_1.peer)

    def json_string_block():
        """creates a main block for testing purposes"""
        prev_hash = "1"
        miner = "2"
        difficulty = "3"

        mb = MainBlock(prev_hash, miner, difficulty, [], [], [])
        # time is automatically set, so we need to change it for the test
        mb.time = 1562228422767
        return mb.string()

    json_string_message = json_string_block()
    time.sleep(10)
    # sends a broadcast message from client 1 to client 2
    p2p_api.send_broadcast(client_1.peer, json_string_message)
    time.sleep(10)
    # sets block_received event
    client_2.event_manager.block_received.set()
    client_3.event_manager.block_received.set()
    assert client_2.p2p_api.get_recv_block(
        peer2.server_info.host) == json_string_message
    assert client_3.p2p_api.get_recv_block(
        peer3.server_info.host) == json_string_message
    time.sleep(3)
    remove_database()
    client_1.p2p_api.event_mg.error.set()
    client_2.p2p_api.event_mg.error.set()
    client_3.p2p_api.event_mg.error.set()


def test_clients_send_tx_broadcast():
    """ test case for broadcasting between two clients"""
    # creates a P2P_API object
    p2p_api = P2P_API()
    # creates a peer named core
    peer = p2p_api.create_a_peer(
        role='core', name='core', host=('0.0.0.0', 8000))
    # creates a dummy peer for testing purposes
    dummy_peer = p2p_api.create_a_peer(
        role="sw", name="switch_1", host=("127.0.0.1", 8011))
    # creates an instance of Client with the specified peer above
    client_1 = Client(create_blockchain(2), peer, dummy_peer)

    # creates a peer named switch_2 with the role sw
    peer2 = p2p_api.create_a_peer(
        role='sw', name='switch_2', host=('0.0.0.0', 8012))
    # creates a Client with the specified peer above and connect it to the peer of client 1
    client_2 = Client(create_blockchain(2), peer2, client_1.peer)
    # creates a peer named switch_3 with the role sw
    peer3 = p2p_api.create_a_peer(
        role='sw', name='switch_3', host=('0.0.0.0', 8013))
    # creates a Client with the specified peer above and connect it to the peer of client 1
    client_3 = Client(create_blockchain(2), peer3, client_1.peer)

    def json_string_tx():
        """creates a main block for testing purposes"""
        sender = "iWVjc8hWuRuePAv1X8nDZdcjKcqivDUH62YKhBXBHqp2yGfgeXyHJDj5XwCHwjWB6GevCjMYT59XSBiQvMYHQ4P"
        receivers = ["01", "02", "0a"]
        amounts = [1, 2, 3]
        fee = 100
        tx = Transaction(sender, receivers, amounts, fee)
        return tx.string()

    json_string_message = json_string_tx()
    time.sleep(15)
    # sends a broadcast message from client 1 to client 2
    p2p_api.send_broadcast(client_1.peer, json_string_message)
    time.sleep(10)
    # sets block_received event
    client_2.event_manager.tx_received.set()
    client_3.event_manager.tx_received.set()
    assert client_2.p2p_api.get_recv_tx(
        peer2.server_info.host) == json_string_message
    time.sleep(3)
    remove_database()
    client_1.p2p_api.event_mg.error.set()
    client_2.p2p_api.event_mg.error.set()


def test_update_chain():
    # creates a P2P_API object
    p2p_api = P2P_API()
    # creates a peer named core
    peer = p2p_api.create_a_peer(
        role='core', name='core', host=('0.0.0.0', 8000))
    # creates a dummy peer for testing purposes
    dummy_peer = p2p_api.create_a_peer(
        role="sw", name="switch_1", host=("127.0.0.1", 8011))
    # creates an instance of Client with the specified peer above
    client_1 = Client(create_blockchain(10), peer, dummy_peer)

    # creates a peer named switch_2 with the role sw
    peer2 = p2p_api.create_a_peer(
        role='sw', name='switch_2', host=('0.0.0.0', 8012))
    # creates a Client with the specified peer above and connect it to the peer of client 1
    client_2 = Client(create_blockchain(16), peer2, client_1.peer)
    # creates a peer named switch_3 with the role sw
    peer3 = p2p_api.create_a_peer(
        role='sw', name='switch_3', host=('0.0.0.0', 8013))
    # creates a Client with the specified peer above and connect it to the peer of client 1
    client_3 = Client(create_blockchain(15), peer3, client_1.peer)


if __name__ == '__main__':
    test_update_chain()
