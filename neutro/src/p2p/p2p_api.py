from typing import List, Tuple

import os
from os import getcwd
from os.path import join
import socket
socket.SO_REUSEPORT = 15

from atomic_p2p.utils.security import self_hash as sh, create_self_signed_cert
from atomic_p2p.peer import Peer


def create_a_peer(role: str, name: str, host: Tuple[str, int]):
    # creates and starts a peer with a specified certificate
    self_hash = sh(join(os.getcwd(), 'atomic_p2p'))

    # Peers must have the same certificate
    cert = create_self_signed_cert(getcwd(), 'data/test.pem', 'data/test.key')
    peer = Peer(host=host, name=name, role=role, cert=cert, _hash=self_hash)
    peer.start()
    return peer


def join_peers(peer_a, peer_b):
    # Sends a join request from peer_a to peer_b
    peer_a.onProcess(['join', '{}:{}'.format(peer_b.server_info.host[0], peer_b.server_info.host[1])])


def send_transaction_broadcast(json_transaction_message: str) -> str:
    # broadcasts a new transaction to a subnet
    return json_transaction_message


def send_block_broadcast(json_block_message: str) -> str:
    # broadcasts a new block to a subnet
    return json_block_message


def send_transaction_direct(self, tx_string: str, from_peer, to_peer):
    # sends a transaction message from a peer to another one
    return {'from_peer': from_peer, 'to_peer': to_peer, 'tx_string': tx_string}


def send_block_direct(self, block_string: str, from_peer, to_peer):
    # sends a block message from a peer to another one
    return {'from_peer': from_peer, 'to_peer': to_peer, 'block_string': block_string}


def receive_transaction_direct(self, from_peer, to_peer):
    # receives a transaction message sent by 'from' peer
    pass


def receive_block_direct(self, from_peer, to_peer):
    # receives a block message sent by 'from' peer
    pass


def send_bootstrap(self, min:int, max:int, blocks: List[str]):
    # sends a set of blocks (min to max) for broadcasting
    return blocks


def request_bootstrap(self, min: int , max: int) -> List[str]:
    # requests a set of blocks for broadcasting
    pass


def request_transaction_broadcast():
    # requests a transaction to broadcast
    pass


def request_block_broadcast():
    # requests a block to broadcast
    pass


def request_transaction_direct():
    # requests a direct transaction between peers
    pass


def request_block_direct():
    # requests a direct block sending between peers
    pass

