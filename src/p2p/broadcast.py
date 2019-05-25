import time
import os
from os import getcwd
from os.path import join
import socket
socket.SO_REUSEPORT = 15

from atomic_p2p.utils.security import self_hash as sh, create_self_signed_cert
from atomic_p2p.peer import Peer

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

    # wait for all threads to complete the join process
    time.sleep(5)

    # send a broadcast message from core to all the directly connected nodes
    nodes['core_1'].onProcess(['send', 'broadcast:sw', 'test'])
    time.sleep(12)

    # stop all the peer threads
    for (_, val) in nodes.items():
        val.stop()


# creates a dictionary for nodes
node = dict()
# creates a core peer
node['core_1'] = Peer(role='core', name='core_1', host=('127.0.0.1', 8000), cert=cert, _hash=self_hash)
# create switch peers
node['switch_1'] = Peer(role='sw', name='switch01', host=('127.0.0.1', 8011), cert=cert, _hash=self_hash)
node['switch_2'] = Peer(role='sw', name='switch02', host=('127.0.0.1', 8012), cert=cert, _hash=self_hash)
node['switch_3'] = Peer(role='sw', name='switch03', host=('127.0.0.1', 8013), cert=cert, _hash=self_hash)
node['switch_4'] = Peer(role='sw', name='switch04', host=('127.0.0.1', 8014), cert=cert, _hash=self_hash)
net(cert, self_hash, node)
