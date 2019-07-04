from neutro.src.p2p.p2p_api import *
from neutro.src.client.client_runner import Client


def p2p_recv_block():
    get_recv_block(init_peer())


def client_running():
    client1 = Client()


def test_recv_event_block():
    event_manager()
    set_events()
    client_running()


if __name__ == '__main__':
    test_recv_event_block()