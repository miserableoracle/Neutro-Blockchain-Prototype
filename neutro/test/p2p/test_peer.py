from neutro.src.p2p.peer import Peer


def test_peer_integration()
    p1 = Peer("0.0.0.0:50505")
    p2 = Peer("0.0.0.0:50506")

    p1.connect(p2)

    p1.send("hi")

    time.sleep(100 / 1000)
    assert p2.handler.last_msg == "hi"


def test_multiple_peer_chain_integration()
    p1 = Peer("0.0.0.0:50501")
    p2 = Peer("0.0.0.0:50502")
    p3 = Peer("0.0.0.0:50503")
    p4 = Peer("0.0.0.0:50504")
    p5 = Peer("0.0.0.0:50505")
    p6 = Peer("0.0.0.0:50506")

    p1.connect(p2)
    p2.connect(p3.endpoint)
    p3.connect(p4.endpoint)
    p4.connect(p5.endpoint)
    p5.connect(p6.endpoint)

    p1.send("hi")

    time.sleep(300 / 1000)

    assert p6.handler.last_msg == "hi"


def test_mesh_peer_integration()
    p1 = Peer("0.0.0.0:50501")
    p2 = Peer("0.0.0.0:50502")
    p3 = Peer("0.0.0.0:50503")
    p4 = Peer("0.0.0.0:50504")
    p5 = Peer("0.0.0.0:50505")
    p6 = Peer("0.0.0.0:50506")

    p1.connect(p2.endpoint)
    p2.connect(p3.endpoint)
    p3.connect(p4.endpoint)
    p3.connect(p5.endpoint)
    p5.connect(p6.endpoint)

    p3.send("hi")

    time.sleep(100 / 1000)

    assert p1.handler.last_msg == "hi"
    assert p4.handler.last_msg == "hi"
    assert p6.handler.last_msg == "hi"


def test_another_thing()
    pass
