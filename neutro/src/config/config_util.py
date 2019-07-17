"""this file has some handy methods for working with configuration"""
from . config import hosts
from neutro.p2p.peer import Peer


def get_peer_list():
    return [Peer(host) for host in hosts]
