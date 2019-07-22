from neutro.src.p2p.p2p_api import P2P_API
from neutro.src.database.p2p_messages_database import get_messages, remove_database
from neutro.src.p2p.peer import Peer
from neutro.src.p2p.neutro_handler import NeutroHandler
import time
import json


def test_peer_integration_broadcast():
    # creates an object of p2p api
    peer1_api = P2P_API()
    # creates a peer through API
    # peer1 = peer1_api.create_a_peer(('0.0.0.0', 8001))

    # creates a peer directly from Peer class
    peer1 = Peer(('0.0.0.0', 8001))
    peer1.start()

    # creates an object of p2p api
    peer2_api = P2P_API()
    # creates a peer
    peer2 = Peer(('0.0.0.0', 8002))
    peer2.start()

    # connects peer 1 to peer 2 through API
    # peer1_api.connect(peer1, peer2)

    # connects peer 1 to peer 2 directly
    peer1.onProcess(['join', '{}:{}'.format(peer2.server_info.host[0], peer2.server_info.host[1])])

    time.sleep(1)
    # checks if the peer 1 has created a net
    assert ('0.0.0.0', 8001) == list(peer2.peer_pool.keys())[0]

    # peer 2 sends a "123" broadcast to connected peers in the net
    peer2_api.send_broadcast(peer2, "123")

    rcv_message = str(get_messages(peer1.server_info.host))
    assert "123" == rcv_message

    time.sleep(5)
    remove_database()
    peer1.stop()
    peer2.stop()


def test_multiple_peer_chain_integration():
    peer_api = P2P_API()
    p1 = Peer(('0.0.0.0', 50501))
    p1.start()

    p2 = Peer(('0.0.0.0', 50502))
    p2.start()

    p3 = Peer(('0.0.0.0', 50503))
    p3.start()

    p4 = Peer(('0.0.0.0', 50504))
    p4.start()

    p5 = Peer(('0.0.0.0', 50505))
    p5.start()

    p6 = Peer(('0.0.0.0', 50506))
    p6.start()

    time.sleep(5)
    p1.onProcess(['join', '{}:{}'.format(p2.server_info.host[0], p2.server_info.host[1])])
    time.sleep(2)
    p2.onProcess(['join', '{}:{}'.format(p3.server_info.host[0], p3.server_info.host[1])])
    time.sleep(2)
    p3.onProcess(['join', '{}:{}'.format(p4.server_info.host[0], p4.server_info.host[1])])
    time.sleep(2)
    p4.onProcess(['join', '{}:{}'.format(p5.server_info.host[0], p5.server_info.host[1])])
    time.sleep(2)
    p5.onProcess(['join', '{}:{}'.format(p6.server_info.host[0], p6.server_info.host[1])])
    time.sleep(2)
    p6.onProcess(['join', '{}:{}'.format(p5.server_info.host[0], p5.server_info.host[1])])

    time.sleep(2)

    peer_api.send_broadcast(p2, "123")
    time.sleep(300 / 1000)
    peer_api.send_broadcast(p3, "123")
    time.sleep(300 / 1000)
    peer_api.send_broadcast(p4, "123")
    time.sleep(300 / 1000)
    peer_api.send_broadcast(p5, "123")
    time.sleep(300 / 1000)
    peer_api.send_broadcast(p6, "123")

    time.sleep(3)

    # checks whether the specific peer is connected with peer/peers
    assert ('0.0.0.0', 50502) == list(p1.peer_pool.keys())[0]
    assert ('0.0.0.0', 50501) == list(p2.peer_pool.keys())[0] and ('0.0.0.0', 50503) == list(p2.peer_pool.keys())[1]
    assert ('0.0.0.0', 50502) == list(p3.peer_pool.keys())[0] and ('0.0.0.0', 50504) == list(p3.peer_pool.keys())[1]
    assert ('0.0.0.0', 50503) == list(p4.peer_pool.keys())[0] and ('0.0.0.0', 50505) == list(p4.peer_pool.keys())[1]
    assert ('0.0.0.0', 50504) == list(p5.peer_pool.keys())[0] and ('0.0.0.0', 50506) == list(p5.peer_pool.keys())[1]
    assert ('0.0.0.0', 50505) == list(p6.peer_pool.keys())[0]

    rcv_message_1 = str(get_messages(p1.server_info.host))
    rcv_message_2 = str(get_messages(p2.server_info.host))
    rcv_message_3 = str(get_messages(p3.server_info.host))
    rcv_message_4 = str(get_messages(p4.server_info.host))
    rcv_message_5 = str(get_messages(p5.server_info.host))
    rcv_message_6 = str(get_messages(p6.server_info.host))

    assert "123" == rcv_message_1 and "123" == rcv_message_2 and "123" == rcv_message_3
    assert "123" == rcv_message_4 and "123" == rcv_message_5
    # assert "123" == rcv_message_6
    remove_database()
    time.sleep(2)
    p1.stop() and p2.stop() and p3.stop() and p4.stop() and p5.stop() and p6.stop()


def test_mesh_peer_integration():
    #ToDo: FIX - can't reach p1 and p6
    peer_api = P2P_API()
    p1 = Peer(('0.0.0.0', 50501))
    p1.start()

    p2 = Peer(('0.0.0.0', 50502))
    p2.start()

    p3 = Peer(('0.0.0.0', 50503))
    p3.start()

    p4 = Peer(('0.0.0.0', 50504))
    p4.start()

    p5 = Peer(('0.0.0.0', 50505))
    p5.start()

    p6 = Peer(('0.0.0.0', 50506))
    p6.start()

    time.sleep(5)
    p1.onProcess(['join', '{}:{}'.format(p2.server_info.host[0], p2.server_info.host[1])])
    time.sleep(2)
    p2.onProcess(['join', '{}:{}'.format(p3.server_info.host[0], p3.server_info.host[1])])
    time.sleep(2)
    p3.onProcess(['join', '{}:{}'.format(p4.server_info.host[0], p4.server_info.host[1])])
    time.sleep(2)
    p3.onProcess(['join', '{}:{}'.format(p5.server_info.host[0], p5.server_info.host[1])])
    time.sleep(2)
    p5.onProcess(['join', '{}:{}'.format(p6.server_info.host[0], p6.server_info.host[1])])

    peer_api.send_broadcast(p3, "123")

    time.sleep(3)


def test_peer_integration_direct():
    # ToDo: assert and try this test for unicast packet sending
    p1 = Peer(('0.0.0.1', 8001))
    p2 = Peer(('0.0.0.2', 8002))

    p2.onProcess(["join", "{0}:{1}".format(p1.server_info.host[0], p1.server_info.host[1]), "123"])
    time.sleep(5)
    p2.onProcess(["send", "{0}:{1}".format(p1.server_info.host[0], p1.server_info.host[1]), "123"])

    print(json.dumps(get_messages(p1.server_info.host)))

    # This statement unicast the packet to target.
    p2.handler_unicast_packet(host=(p1.server_info.host[0], p1.server_info.host[1]), pkt_type=NeutroHandler.pkt_type)
