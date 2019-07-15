"""This class implements the client runner. It manages a lot of things:

Voting:
    -Vote for the first block that has been seen
PoW
    -when 2/3 + 1 of all shard blocks are there start PoW
    -publish block when found
    -abort if new block is published
    -adjust difficulty if blocks are beeing produced to fast or to slow
        -periodically once a day/week/lunar/month
p2p
    -broadcast and send blocks and tx to other nodes
    -receive requests (event manager)
"""

import threading
from neutro.src.util import loggerutil
from neutro.src.database import wallet_database
from neutro.src.client.transaction_pool import Pool
from neutro.src.p2p.p2p_api import P2P_API
import time


class Client(threading.Thread):
    """this class does all the previously described tasks"""

    def __init__(self, chain, peer_init, connected_to=None):
        threading.Thread.__init__(self)
        self.p2p_api = P2P_API()
        self.stop = threading.Event()
        self.wallet = wallet_database.load_wallet()
        self.event_manager = self.p2p_api.event_mg
        # initiate the peer from the peer_init if it is called with peer or otherwise initiate here
        self.peer = peer_init # or self.p2p_api.create_a_peer(role="myself", name=self.wallet.get_address(), host=("127.0.0.1", 8012))
        self.peer_host = self.peer.server_info.host
        self.pool = Pool()
        self.chain = chain
        self.start()

        if connected_to is not None:
            self.connect_to = connected_to

    def run(self):
        loggerutil.debug("client started")

        # blocking call, connects this peer to other known peers
        self.p2p_api.connect(self.peer, self.connect_to)

        loggerutil.debug("client connected")

        #  blocking call
        current_height = len(self.chain) - 1

        client_net = self.p2p_api.list_peers_in_net(self.peer)
        loggerutil.debug("Client with host {0} - Current state of the net {1}".format(self.peer_host, client_net))
        block_list = self.p2p_api.update_chain(current_height, self.peer_host, client_net)

        # non blocking
        self.p2p_api.update_block_pool()

        # not blocking call because 2 peers could have different versions of
        # the pool
        self.p2p_api.update_tx_pool()

        # loggerutil.debug("client init update")

        self.loop()

    def loop(self):
        """this method loops for ever until it is stopped by force or with the "stop" event"""
        while True:
            if self.stop.isSet():
                loggerutil.debug("shutting down client")
                break
            if self.manage_events():
                loggerutil.debug("shutting down client due to an error")
                break

            # start of the pow

    def validate_block(block: str) -> bool:
        """a lot of steps to validate if a block is correct"""
        return True

    def validate_tx(tx: str) -> bool:
        """a lot of steps to validate if a tx is correct"""
        return True

    def manage_events(self) -> bool:
        """
        Manages all functionality that has to be asynchronous.
        All these events can be set by the p2p api, the client then handles these events in its own thread

        returns a bool that is only True if the client needs to be shut down in case of an error
        """
        # get data from the p2p
        if self.event_manager.block_received.isSet():
            block = self.p2p_api.get_recv_block(self.peer_host)
            loggerutil.debug("block received event is triggered by: {0}:".format(self.peer_host))
            loggerutil.debug("Block string: {0}".format(block))
            # do stuff
            self.event_manager.block_received.clear()

        if self.event_manager.tx_received.isSet():
            tx = self.p2p_api.get_recv_tx(self.peer_host)
            loggerutil.debug("transaction received event is triggered by: {0}:".format(self.peer_host))
            loggerutil.debug("Tx string: {0}".format(tx))
            # do stuff
            self.event_manager.tx_received.clear()

        if self.event_manager.tx_pool_received.isSet():
            tx_pool = self.p2p_api.get_recv_tx_pool()
            # do stuff
            self.event_manager.tx_pool_received.clear()

        if self.event_manager.bootstr_received.isSet():
            bootstr = self.p2p_api.get_recv_bootstr()
            # do stuff
            self.event_manager.bootstr_received.clear()

        # give data to the p2p
        if self.event_manager.height_request.isSet():
            client_height = len(self.chain) - 1
            self.p2p_api.send_height(self.peer_host, client_height)
            # do stuff
            self.event_manager.height_request.clear()

        if self.event_manager.block_request.isSet():
            # returns list of requested block numbers
            number_list = self.p2p_api.get_requ_block_numbers()
            # get the highest block from the number list
            last_num_from_list = number_list[-1]
            # check if the highest blockchain of a client is the same as from the list
            if len(self.chain) == last_num_from_list:
                # send the blocks that are missing from smaller chains
                for number in number_list:
                    self.p2p_api.send_block(number, self.chain[number-1])
            # do stuff
            self.event_manager.block_request.clear()

        if self.event_manager.tx_request.isSet():
            # do stuff
            self.event_manager.tx_request.clear()

        if self.event_manager.tx_pool_request.isSet():
            self.p2p_api.send_pool(self.pool.string())
            self.event_manager.tx_pool_request.clear()

        if self.event_manager.bootstr_request.isSet():
            from_block_number, to_block_number, reciever = self.p2p_api.get_requ_bootstr_numbers()
            temp = []
            # fill temp with the blocks from and to
            self.p2p_api.send_bootstr(reciever, temp)
            # do stuff
            self.event_manager.bootstr_request.clear()

        if self.event_manager.connection_lost.isSet():
            # reconnect maybe ?
            # do stuff
            self.event_manager.connection_lost.clear()

        if self.event_manager.error.isSet():
            loggerutil.debug("shutdown event is triggered")
            # loggerutil.error(self.p2p_api.get_error_message())
            # shut down the client after logging the error
            self.p2p_api.stop_peer_thread(self.peer)
            return True

        return False

    def send_event_manager(self):
        """returns event_manager object of client"""
        self.p2p_api.em(self.event_manager)

