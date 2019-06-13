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
from neutro.src.p2p.peer_database import store_neighbors
from neutro.src.p2p.peer_database import get_neighbors


json_string_transaction = test_transaction()
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
    nodes['switch_3'].onProcess(['join', '127.0.0.1:{}'.format(nodes['switch_2'].server_info.host[1])])
    nodes['switch_4'].onProcess(['join', '127.0.0.1:{}'.format(nodes['core_1'].server_info.host[1])])

    # wait for all threads to complete the join process
    time.sleep(5)

    def direct_nodes_of(node_a_hostname):
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

    def indirect_nodes_of(node_a_hostname):
        # returns and stores a list of hosts indirectly connected to a given node
        values = get_neighbors(nodes[node_a_hostname].server_info.name)
        for nds in values:
            direct_nodes_of(nodes[nds].server_info.name)

    indirect_nodes_of(nodes['core_1'].server_info.name)

    # send a broadcast message from core to all the directly connected nodes
    nodes['core_1'].onProcess(['send', 'broadcast:sw', json_string_transaction])

    time.sleep(12)

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

net(cert, self_hash, node)
