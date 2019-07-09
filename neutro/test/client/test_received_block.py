from neutro.src.p2p.p2p_api import *
from neutro.src.client.client_runner import Client


def p2p_recv_block():
    get_recv_block(init_peer())


def test_recv_event_block():
    client1 = Client()


if __name__ == '__main__':
    test_recv_event_block()
