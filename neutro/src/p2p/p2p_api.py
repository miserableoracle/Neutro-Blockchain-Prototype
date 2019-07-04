import socket
socket.SO_REUSEPORT = 15

from typing import List, Tuple, Dict
from atomic_p2p.peer.entity.peer_info import PeerInfo
import os
from os import getcwd
from os.path import join
from atomic_p2p.utils.security import self_hash as sh, create_self_signed_cert
from neutro.src.database.peer_database import store_neighbors
from neutro.src.database.peer_database import get_neighbors
from neutro.src.p2p.peer import Peer
from neutro.src.p2p.neutro_handler import NeutroHandler
import re
import time
from neutro.src.util import loggerutil
from neutro.src.client.event_manager import EventManager
from neutro.src.database.p2p_messages_database import get_messages
from neutro.src.database.block_database import *


def init_peer():
    return create_a_peer(role='core', name='core', host=('127.0.0.1', 8011))


def event_manager():
    event_mg = EventManager()
    return event_mg


def set_block_received_event():
    em = event_manager()
    em.block_received.set()


def create_a_peer(role: str, name: str, host: Tuple[str, int]):
    # creates and starts a peer with a specified certificate
    self_hash = sh(join(os.getcwd()))

    # Peers must have the same certificate
    cert = create_self_signed_cert(getcwd(), 'data/certificate.pem', 'data/private.key')
    peer = Peer(host=host, name=name, role=role, cert=cert, _hash=self_hash)
    peer.start()

    time.sleep(10)
    peer.stop()

    return peer


def stop_peer_thread(peer):
    # stops a started peer thread
    time.sleep(5)
    peer.stop()


def join_peers(peer_a: Peer, peer_b: Peer):
    # Sends a join request from peer_a to peer_b
    peer_a.onProcess(['join', '{}:{}'.format(
        peer_b.server_info.host[0], peer_b.server_info.host[1])])


def connect(peer: Peer, connect_to_peer=None):
    # connects a peer to existing peers

    core_peer = init_peer()
    #  returns connect_to_peer if a peer to be connected is set and otherwise returns an initiated peer
    peer2 = connect_to_peer or core_peer

    # add a peer in the net
    join_peers(peer, peer2)

    # set block received event
    set_block_received_event()
    loggerutil.debug("set block received event")


def update_chain(current_height):
    pass


def update_tx_pool():
    pass


def send_height(height):
    return height


def get_recv_block(peer):
    # gets the stored message of the peer received by
    return get_messages(peer.server_info.host)


def get_requ_block_numbers():
    return


def get_requ_bootstr_numbers():
    pass


def get_recv_tx():
    pass


def get_recv_tx_pool():
    pass


def get_recv_bootstr():
    pass


def list_peers_in_net(core: Peer) -> Dict[Tuple[str, int], PeerInfo]:
    # lists all peers currently available in the net
    return core.peer_pool


def send_broadcast(nodes, from_node, json_transaction_message: str):
    # broadcasts a new transaction to a subnet

    def direct_nodes_of(node_a_hostname: str) -> List[str]:
        # returns and stores a list of hosts directly connected to a given node
        node_a = nodes[node_a_hostname].connectlist
        node_a = list(node_a)

        # create a list of hostname only
        direct_nodes_of_a = []

        for dNodes in node_a:
            # gets only the hostname of PeerInfo object
            m = re.search('name=(.+?),', str(dNodes))
            if m:
                found = m.group(1)
                direct_nodes_of_a.append(found)

        store_neighbors(
            nodes[node_a_hostname].server_info.name, direct_nodes_of_a)
        return direct_nodes_of_a

    direct_nodes_of(from_node.server_info.name)

    def indirect_nodes_of(node_a_hostname: str):
        # returns and stores a list of hosts indirectly connected to a given
        # node

        # gets the neighbors of core node
        values = get_neighbors(nodes[node_a_hostname].server_info.name)
        for nds in values:
            # gets the of all the direct neighbors of core
            direct_nodes_of(nodes[nds].server_info.name)

            # sends a broadcast transaction message from a node to other
            # directly connected nodes except the core node
            nodes[nds].handler_broadcast_packet(
                host=(None, "sw"), pkt_type=NeutroHandler.pkt_type, **{
                    "msg": json_transaction_message
                })

    indirect_nodes_of(from_node.server_info.name)

    # send a broadcast transaction message from core to all the directly
    # connected nodes
    from_node.handler_broadcast_packet(
        host=(None, "sw"), pkt_type=NeutroHandler.pkt_type, **{
            "msg": json_transaction_message
        })


def send_transaction_direct(json_string_transaction: str, from_peer, to_peer):
    # Send a transaction message from one peer to the other
    from_peer.onProcess(['send', '{}:{}'.format(to_peer.server_info.host[0], to_peer.server_info.host[1]),
                         json_string_transaction])


def send_block_direct(json_block_string: str, from_peer, to_peer):
    # sends a block message from a peer to another one
    from_peer.onProcess(['send', '{}:{}'.format(to_peer.server_info.host[0], to_peer.server_info.host[1]),
                         json_block_string])


def send_bootstrap(min: int, max: int, blocks: List[str]):
    # sends a set of blocks (min to max) for broadcasting
    return blocks

