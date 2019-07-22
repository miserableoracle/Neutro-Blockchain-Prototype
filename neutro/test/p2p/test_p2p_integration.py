from neutro.src.client.client_runner import Client
from neutro.src.p2p.peer import Peer
import time
from neutro.src.chain.main_block import MainBlock
from neutro.src.database.p2p_messages_database import remove_database

"""
def test_get_difficulty():
    c1 = Client()
    c1.difficulty = "test_diff"

    p2p2 = P2P_API()

    p2p2.connect(c1.peer.endpoint)

    assert p2p2.get_difficulty() == "test_diff"


def test_get_current_height():
	c1 = Client()
    c1.height = 1918349

    p2p2 = P2P_API()

    p2p2.connect(c1.peer.endpoint)

    assert p2p2.get_current_height() == 1918349
"""


def test_send_main_block():

	client1 = Client()

	peer1 = Peer(('0.0.0.0', 8001))
	peer1.start()
	peer2 = Peer(('0.0.0.0', 8002))
	peer2.start()

	def block():
		"""creates a main block for testing purposes"""
		prev_hash = "1"
		miner = "2"
		difficulty = "3"

		mb = MainBlock(prev_hash, miner, difficulty, [], [], [])
		# time is automatically set, so we need to change it for the test
		mb.time = 1562228422767
		mb.height = 1
		return mb

	# client1.main_block_pool.add_block(block())

	client2 = Client()
	# connects peer 1 to peer 2 through client's API
	client1.p2p_api.connect(peer1, peer2)


	# ToDo: use this instead
	# assert client2.main_block_pool.contains(someblock)
	json_string_message = block().string()

	time.sleep(10)
	# sends a broadcast message from client 1 to client 2
	client1.p2p_api.send_broadcast(peer1, json_string_message)
	time.sleep(10)
	# sets block_received event
	client2.event_manager.block_received.set()

	assert client2.p2p_api.get_recv_block(peer2.server_info.host) == json_string_message
	time.sleep(3)
	# remove the data
	remove_database()
	# stop the event
	client2.p2p_api.event_mg.error.set()


def test_send_shard_block():
	pass

def test_send_tx():
	pass

def test_send_vtx():
	pass

def test_send_vote():
	pass
	# tbd later


def test_send_peer():
	pass
	# tbd later

"""
def test_send_main_block_pool():
	client1 = Client()
	client1.start()

	client2 = Client()
	client2.connect(client1)

	peer1 = Peer(('0.0.0.0', 8001))
	peer2 = Peer(('0.0.0.0', 8002))

	# connects peer 1 to peer 2 through cleAPI
	client1.p2p_api.connect(peer1, peer2)
	# peer1_api.connect(peer1, peer2)

	def create_a_block():
		prev_hash = "1"
		miner = "2"
		difficulty = "3"

		mb = MainBlock(prev_hash, miner, difficulty, [], [], [])
		# time is automatically set, so we need to change it for the test
		mb.time = 1562228422767
		return mb


	client1.main_block_pool.add(create_a_block())
	client1.main_block_pool.add(some2)
	client1.main_block_pool.add(some3)
	client1.main_block_pool.add(some4)

	client2.start()

	time.sleep(1)

	assert c2.main_block_pool.contains(some1 and some2 and some3 and some4)
"""
def test_send_shard_block_pool():
	pass

def test_send_tx_pool():
	pass

def test_update_vtx_pool():
	pass

def test_send_vote_pool():
	pass
	# tbd later

"""
def test_api_set_get_block_event():
	api1
	api2

	api1.connect(api2)

	api1.get_block(100)

	assert api2.event_mgr.get_block.isSet()



for event in event_mgr:
	def test_api_set_event_name():
"""
