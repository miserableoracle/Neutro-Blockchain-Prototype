from typing import List
from typing import NewType
from atomic_p2p.utils.security import self_hash as sh, create_self_signed_cert
from atomic_p2p.peer import Peer
import time
import os
from os import getcwd
from os.path import join
import socket


def create_a_peer(role:str, name: str, host):
    # creates a peer with a specified certificate
    self_hash = sh(join(os.getcwd(), 'atomic_p2p'))

    # Peers must have the same certificate
    cert = create_self_signed_cert(getcwd(), 'data/test.pem', 'data/test.key')

    peer_instance = Peer(role=role, name=name, host=host, cert=cert, self_hash=self_hash)

    return peer_instance


def send_transaction_broadcast(self, json_transaction_message:str) -> str:
    # broadcasts a new transaction to a subnet
    return self.json_transaction_message


def send_block_broadcast(self, json_block_message:str) -> str:
    # broadcasts a new block to a subnet
    return self.json_block_message


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


def bootstrapping(self, min:int, max:int, block: List[str]):
    # sends a set of blocks (min to max) for broadcasting
    pass





