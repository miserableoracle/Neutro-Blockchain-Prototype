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


class P2P_API():

    def __init__(self):
        """creates an event manager object"""
        self.event_mg = EventManager()
        self.connected_peer_list = {}
        self.peers_dict = {}

    def init_peer(self):
        return self.create_a_peer(role='core', name='core', host=('0.0.0.0', 8015))

    def create_a_peer(self, role: str, name: str, host: Tuple[str, int]):
        """creates and starts a peer with a specified certificate"""
        self_hash = sh(join(os.getcwd()))

        # Peers must have the same certificate
        cert = create_self_signed_cert(getcwd(), 'data/certificate.pem', 'data/private.key')
        peer = Peer(host=host, name=name, role=role, cert=cert, _hash=self_hash)
        peer.start()
        # time.sleep(10)
        # peer.stop()

        return peer

    def stop_peer_thread(self, peer):
        """stops a started peer thread"""
        self.event_mg.error.set()
        time.sleep(5)
        peer.stop()

    def join_peers(self, peer_a: Peer, peer_b: Peer):
        """sends a join request from peer_a to peer_b"""
        peer_a.onProcess(['join', '{}:{}'.format(
            peer_b.server_info.host[0], peer_b.server_info.host[1])])

    def connect(self, peer: Peer, connect_to_peer=None):
        """connects a peer to existing peers"""

        core_peer = self.init_peer()
        #  returns connect_to_peer if a peer to be connected is set and otherwise returns an initiated peer
        peer2 = connect_to_peer or core_peer

        # add a peer in the net
        self.join_peers(peer, peer2)
        time.sleep(5)
        self.connected_peer_list = self.list_peers_in_net(core_peer).keys()
        self.peers_dict.update({peer.server_info.host: 0})

        # self.event_mg.block_received.set()

    def update_chain(self, current_height):
        loggerutil.debug("Current height {0}".format(current_height))
        core_peer = self.init_peer()
        pass

    def update_tx_pool(self):
        pass

    def send_height(self, height):
        return height

    def get_recv_block(self, peer):
        """ gets the stored message of the peer received by"""
        return get_messages(peer.server_info.host)

    def get_requ_block_numbers(self):
        pass

    def get_requ_bootstr_numbers(self):
        pass

    def get_recv_tx(self):
        pass

    def get_recv_tx_pool(self):
        pass

    def get_recv_bootstr(self):
        pass

    def update_block_pool(self):
        pass

    def list_peers_in_net(self, core: Peer) -> Dict[Tuple[str, int], PeerInfo]:
        """lists all peers currently available in the net"""
        return core.peer_pool

    def send_broadcast(self, nodes, from_node, json_transaction_message: str):
        """broadcasts a new transaction to a subnet"""

        def direct_nodes_of(node_a_hostname: str) -> List[str]:
            """returns and stores a list of hosts directly connected to a given node"""
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
            """returns and stores a list of hosts indirectly connected to a given node"""

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

    def send_transaction_direct(self, json_string_transaction: str, from_peer, to_peer):
        """send a transaction message from one peer to the other"""
        from_peer.onProcess(['send', '{}:{}'.format(to_peer.server_info.host[0], to_peer.server_info.host[1]),
                             json_string_transaction])

    def send_block_direct(self, json_block_string: str, from_peer, to_peer):
        """sends a block message from a peer to another one"""
        from_peer.onProcess(['send', '{}:{}'.format(to_peer.server_info.host[0], to_peer.server_info.host[1]),
                             json_block_string])

    def send_bootstrap(self, min: int, max: int, blocks: List[str]):
        """sends a set of blocks (min to max) for broadcasting"""
        return blocks




