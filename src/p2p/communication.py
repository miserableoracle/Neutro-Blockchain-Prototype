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

# Create a peer named core01 with the address 127.0.0.1:8000
core = Peer(role='core', name='core01', host=('127.0.0.1', 8000), cert=cert, _hash=self_hash)
# Starts the thread’s activity
core.start()

# Create a peer named switch01 with the address 127.0.0.1:8010
switch = Peer(role='sw', name='switch01', host=('127.0.0.1', 8010), cert=cert, _hash=self_hash)

# Starts the thread’s activity
switch.start()

# Sends a join request to core peer
switch.onProcess(['join', '127.0.0.1:{}'.format(core.server_info.host[1])])
time.sleep(5)

# Send a message (123) from switch01 peer to core peer
switch.onProcess(['send', '127.0.0.1:{}'.format(core.server_info.host[1]), '123'])
time.sleep(5)

