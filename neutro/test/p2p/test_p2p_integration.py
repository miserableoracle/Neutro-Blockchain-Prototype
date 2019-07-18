

def test_get_difficulty():
    c1 = Client()
    c1.difficulty = "test_diff"

    p2p2 = P2P_API()

    p2p2.connect(c1.peer.endpoint)

    assert p2p2.get_difficulty() == "test_diff"


def test_get_current_height():
	c1 = Client()
    c1.heigth = 1918349

    p2p2 = P2P_API()

    p2p2.connect(c1.peer.endpoint)

    assert p2p2.get_current_height() == 1918349

def test_send_main_block():
	c1 = Client()
	c1.main_block_pool.add(someblock)


	c2 = Client()
	c2.connect(c1.peer.endpoint)

	assert c2.main_block_pool.contains(someblock)

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

def test_send_main_block_pool():
	c1 = Client()
	c1.start()
	
	c2 = Client()
	c2.connect(c1)
	
	c1.main_block_pool.add(some1)
	c1.main_block_pool.add(some2)
	c1.main_block_pool.add(some3)
	c1.main_block_pool.add(some4)
	
	c2.start()

	time.sleep(1)

	assert c2.main_block_pool.contains(some1 and some2 and some3 and some4)

	pass

def test_send_shard_block_pool():
	pass

def test_send_tx_pool():
	pass

def test_update_vtx_pool():
	pass

def test_send_vote_pool():
	pass
	# tbd later


def test_api_set_get_block_event():
	api1
	api2

	api1.connect(api2)

	api1.get_block(100)

	assert api2.event_mgr.get_block.isSet()
