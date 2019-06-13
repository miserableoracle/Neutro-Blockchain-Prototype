import time
import os
from os import getcwd
from os.path import join
import socket
socket.SO_REUSEPORT = 15
import re

from atomic_p2p.utils.security import self_hash as sh, create_self_signed_cert
from atomic_p2p.peer import Peer

from neutro.src.p2p.p2p_transaction import test_transaction
from neutro.src.p2p.p2p_block import test_block
from neutro.src.p2p.peer_database import store_neighbors
from neutro.src.p2p.peer_database import get_neighbors
from typing import List


json_string_transaction = test_transaction()
json_string_block = test_block()

self_hash = sh(join(os.getcwd(), 'atomic_p2p'))

# Peers must have the same certificate
cert = create_self_signed_cert(getcwd(), 'data/test.pem', 'data/test.key')


def net(cert, self_hash, nodes):
    """broadcasts a message to all the nodes directly connected to core 1 node"""

    # start all the peer threads
    for (_, val) in nodes.items():
        val.start()

    nodes['switch_1'].onProcess(['join', '127.0.0.1:{}'.format(nodes['core_1'].server_info.host[1])])
    nodes['switch_2'].onProcess(['join', '127.0.0.1:{}'.format(nodes['core_1'].server_info.host[1])])
    nodes['switch_3'].onProcess(['join', '127.0.0.1:{}'.format(nodes['core_1'].server_info.host[1])])
    nodes['switch_4'].onProcess(['join', '127.0.0.1:{}'.format(nodes['core_1'].server_info.host[1])])
    nodes['switch_5'].onProcess(['join', '127.0.0.1:{}'.format(nodes['switch_4'].server_info.host[1])])
    nodes['switch_6'].onProcess(['join', '127.0.0.1:{}'.format(nodes['switch_4'].server_info.host[1])])

    # wait for all threads to complete the join process
    time.sleep(10)

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

        store_neighbors(nodes[node_a_hostname].server_info.name, direct_nodes_of_a)
        return direct_nodes_of_a

    direct_nodes_of(nodes['core_1'].server_info.name)

    def indirect_nodes_of(node_a_hostname: str):
        # returns and stores a list of hosts indirectly connected to a given node

        # gets the neighbors of core node
        values = get_neighbors(nodes[node_a_hostname].server_info.name)
        for nds in values:
            # gets the of all the direct neighbors of core
            direct_nodes_of(nodes[nds].server_info.name)

            # sends a broadcast transaction message from a node to other directly connected nodes except the core node
            nodes[nds].onProcess(['send', 'broadcast:sw', json_string_transaction])

            # send a broadcast block message from core to other directly connected nodes except the core node
            nodes[nds].onProcess(['send', 'broadcast:sw', json_string_block])

    indirect_nodes_of(nodes['core_1'].server_info.name)

    # send a broadcast transaction message from core to all the directly connected nodes
    nodes['core_1'].onProcess(['send', 'broadcast:sw', json_string_transaction])

    # send a broadcast block message from core to all the directly connected nodes
    nodes['core_1'].onProcess(['send', 'broadcast:sw', json_string_block])

    time.sleep(10)

    # stop all the peer threads
    for (_, val) in nodes.items():
        val.stop()


# creates a dictionary for nodes
node = dict()
# creates a core peer
node['core_1'] = Peer(role='core', name='core_1', host=('127.0.0.1', 8000), cert=cert, _hash=self_hash)
# create switch peers
node['switch_1'] = Peer(role='sw', name='switch_1', host=('127.0.0.1', 8011), cert=cert, _hash=self_hash)
node['switch_2'] = Peer(role='sw', name='switch_2', host=('127.0.0.1', 8012), cert=cert, _hash=self_hash)
node['switch_3'] = Peer(role='sw', name='switch_3', host=('127.0.0.1', 8013), cert=cert, _hash=self_hash)
node['switch_4'] = Peer(role='sw', name='switch_4', host=('127.0.0.1', 8014), cert=cert, _hash=self_hash)
node['switch_5'] = Peer(role='sw', name='switch_5', host=('127.0.0.1', 8015), cert=cert, _hash=self_hash)
node['switch_6'] = Peer(role='sw', name='switch_6', host=('127.0.0.1', 8016), cert=cert, _hash=self_hash)

net(cert, self_hash, node)
