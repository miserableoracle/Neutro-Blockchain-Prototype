from neutro.src.database.client_chain_heights_database import store_client_chain_height, get_client_chain_height
from neutro.src.database.p2p_messages_database import get_messages, remove_database
from neutro.src.client.event_manager import EventManager
from neutro.src.util import loggerutil
import time
import re
from neutro.src.p2p.neutro_handler import NeutroHandler
from neutro.src.p2p.peer import Peer
from neutro.src.database.peer_database import get_neighbors
from neutro.src.database.peer_database import store_neighbors
from atomic_p2p.utils.security import self_hash as sh, create_self_signed_cert
from os.path import join
from os import getcwd
import os
from atomic_p2p.peer.monitor import Monitor
from atomic_p2p.peer.entity.peer_info import PeerInfo
from typing import List, Tuple, Dict
import json
import socket
socket.SO_REUSEPORT = 15


class P2P_API():

    def __init__(self):
        """creates an event manager object"""
        self.event_mg = EventManager()
        self.client_chains = {}
        self.numbers_block = []
        self.client_chains_string = {}

    def init_peer(self):
        return self.create_a_peer(role="sw", name="switch_1", host=("127.0.0.1", 8011))

    def create_a_peer(self, role: str, name: str, host: Tuple[str, int]):
        """creates and starts a peer with a specified certificate"""
        self_hash = sh(join(os.getcwd()))

        # Peers must have the same certificate
        cert = create_self_signed_cert(
            getcwd(), 'data/certificate.pem', 'data/private.key')
        peer = Peer(host=host, name=name, role=role,
                    cert=cert, _hash=self_hash)
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

        # self.event_mg.block_received.set()

    def update_chain(self, client_height, client_host, client_net):
        # trigger height request of the client
        self.event_mg.height_request.set()

        # for each client in the network get the current height from db
        # store it as a dictionary with host as a key and their height as a value
        for host in client_net:
            self.client_chains.update({host: get_client_chain_height(host)})

        # go over all of the clients in the net
        for other_host, other_height in self.client_chains.items():
            # check their height against the actual client height
            if other_height > client_height:
                self.numbers_block = list(
                    range(client_height+1, other_height+1))
                self.event_mg.block_request.set()
                #ToDo: send bootstrap broadcast from client_height+1 to other_height

    def update_tx_pool(self):
        pass

    def send_height(self, client_host, client_height):
        store_client_chain_height(client_host, client_height)

    def get_recv_block(self, peer_host):
        """ gets the stored message of the peer received by"""
        json_get_message = json.dumps(get_messages(peer_host))
        return json_get_message

    def get_requ_block_numbers(self):
        return self.numbers_block

    def get_requ_bootstr_numbers(self):
        pass

    def get_recv_tx(self, peer_host):
        json_get_message = json.dumps(get_messages(peer_host))
        return json_get_message

    def get_recv_tx_pool(self):
        pass

    def get_recv_bootstr(self):
        pass

    def update_block_pool(self):
        pass

    def get_error_message(self):
        pass

    def list_peers_in_net(self, core: Peer) -> Dict[Tuple[str, int], PeerInfo]:
        """lists all peers currently available in the net"""
        return core.peer_pool.keys()

    def send_broadcast(self, from_node, json_message: str):
        """broadcasts a new message to a subnet"""

        def direct_nodes_of(node_a_hostname: str) -> List[str]:
            """returns and stores a list of hosts directly connected to a given node"""

            node_a = from_node.connectlist
            node_a = list(node_a)
            print("Node_a{0}".format(node_a))
            # create a list of hostname only
            direct_nodes_of_a = []

            for dNodes in node_a:
                # gets only the hostname of PeerInfo object
                m = re.search('name=(.+?),', str(dNodes))
                if m:
                    found = m.group(1)
                    direct_nodes_of_a.append(found)
            print("direct_nodes_of_a:{0}".format(direct_nodes_of_a))
            store_neighbors(
                from_node.server_info.name, direct_nodes_of_a)
            return direct_nodes_of_a

        direct_nodes_of(from_node)

        def indirect_nodes_of(node_a: str):
            """returns and stores a list of hosts indirectly connected to a given node"""

            # gets the neighbors of core node
            values = get_neighbors(node_a.server_info.name)
            for nds in values:
                # gets the of all the direct neighbors of core
                direct_nodes_of(nds)

                # sends a broadcast transaction message from a node to other
                # directly connected nodes except the core node
                self.init_peer().handler_broadcast_packet(
                    host=(None, "sw"), pkt_type=NeutroHandler.pkt_type, **{
                        "msg": json_message
                    })
        #ToDo: fix indirect nodes - client peers
        #indirect_nodes_of(from_node)

        # send a broadcast transaction message from core to all the directly
        # connected nodes
        from_node.handler_broadcast_packet(
            host=(None, "all"), pkt_type=NeutroHandler.pkt_type, **{
                "msg": json_message
            })

    def send_bootstrap(self, min: int, max: int, blocks: List[str]):
        """sends a set of blocks (min to max) for broadcasting"""
        return blocks

    def send_block(self, number, the_block_to_number):
        self.client_chains.update({number: the_block_to_number})
