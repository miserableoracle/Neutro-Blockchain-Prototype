import os
from os import getcwd
from os.path import join
import time

# Socket problem on my PC workaround FIX
import socket
socket.SO_REUSEPORT = 15

from atomic_p2p.peer import Peer
from atomic_p2p.utils.security import self_hash as sh, create_self_signed_cert


def self_hash():
    return sh(join(os.getcwd(), 'atomic_p2p'))


def cert():
    return create_self_signed_cert(getcwd(), 'data/test.pem', 'data/test.key')


def default_peer(cert, self_hash):
    p = Peer(host=('0.0.0.0', 8000), name='node', role='role', cert=cert, _hash=self_hash)
    p.start()
    time.sleep(1)
    p.stop()


if __name__ == "__main__":
    hash_value = self_hash()
    certificate_value = cert()
    default_peer(certificate_value, hash_value)


