from neutro.src.client.client_runner import Client
from neutro.src.p2p.p2p_api import P2P_API
from neutro.src.chain.main_block import MainBlock
from neutro.src.chain.transaction import Transaction
from neutro.src.util import loggerutil
import pytest
import time


def test_clients_send_block_broadcast():
    """ test case for broadcasting between two clients"""
    # creates a P2P_API object
    p2p_api = P2P_API()
    # creates a peer named core
    peer = p2p_api.create_a_peer(role='core', name='core', host=('0.0.0.0', 8000))
    # creates an instance of Client with the specified peer above
    client_1 = Client(peer)

    # creates a peer named switch_2 with the role sw
    peer2 = p2p_api.create_a_peer(role='sw', name='switch_2', host=('0.0.0.0', 8012))
    # creates a Client with the specified peer above
    client_2 = Client(peer2)

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
    # sets block_received event
    client_1.event_manager.block_received.set()

    time.sleep(5)


def test_clients_send_tx_broadcast():
    """ test case for broadcasting between two clients"""
    # creates a P2P_API object
    p2p_api = P2P_API()
    # creates a peer named core
    peer = p2p_api.create_a_peer(role='core', name='core', host=('0.0.0.0', 8000))
    # creates an instance of Client with the specified peer above
    client_1 = Client(peer)

    # creates a peer named switch_2 with the role sw
    peer2 = p2p_api.create_a_peer(role='sw', name='switch_2', host=('0.0.0.0', 8012))
    # creates a Client with the specified peer above
    client_2 = Client(peer2)

    def json_string_tx():
        """creates a main block for testing purposes"""
        sender = "iWVjc8hWuRuePAv1X8nDZdcjKcqivDUH62YKhBXBHqp2yGfgeXyHJDj5XwCHwjWB6GevCjMYT59XSBiQvMYHQ4P"
        receivers = ["01", "02", "0a"]
        amounts = [1, 2, 3]
        fee = 100
        tx = Transaction(sender, receivers, amounts, fee)
        return tx.string()

    json_string_message = json_string_tx()
    time.sleep(10)
    # sends a broadcast message from client 1 to client 2
    p2p_api.send_broadcast(client_1.peer, json_string_message)
    # sets block_received event
    client_1.event_manager.tx_received.set()

    time.sleep(5)


def test_update_chain():
    pass

