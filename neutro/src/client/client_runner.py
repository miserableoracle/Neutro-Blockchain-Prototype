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

import time
import threading
from neutro.src.util import loggerutil
from neutro.src.database import wallet_database, block_database
from neutro.src.client.event_manager import EventManager
from neutro.src.client.transaction_pool import Pool
from neutro.src.p2p import p2p_api


class Client(threading.Thread):
    """this class does all the previously described tasks"""

    def __init__(self):
        threading.Thread.__init__(self)
        self.stop = threading.Event()
        self.wallet = wallet_database.load_wallet()
        self.event_manager = p2p_api.event_manager()
        self.peer = p2p_api.create_a_peer(
            role="myself", name=self.wallet.get_address(), host=("127.0.0.1", 8000))
        self.pool = Pool()
        self.start()

    def run(self):
        loggerutil.debug("client started")

        # blocking call, connects this peer to other known peers
        p2p_api.connect(self.peer)
        loggerutil.debug("client connected")

        # not blocking call because 2 peers could have different versions of
        # the chain
        p2p_api.update_chain(block_database.get_current_height())

        # not blocking call because 2 peers could have different versions of
        # the pool
        p2p_api.update_tx_pool()

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
        loggerutil.debug("getting the data from p2p...")
        if self.event_manager.block_received.isSet():
            block = p2p_api.get_recv_block(self.peer)
            loggerutil.debug("block received event is triggered")
            # do stuff
            self.event_manager.block_received.clear()

        if self.event_manager.tx_received.isSet():
            tx = p2p_api.get_recv_tx()
            # do stuff
            self.event_manager.tx_received.clear()

        if self.event_manager.tx_pool_received.isSet():
            tx_pool = p2p_api.get_recv_tx_pool()
            # do stuff
            self.event_manager.tx_pool_received.clear()

        if self.event_manager.bootstr_received.isSet():
            bootstr = p2p_api.get_recv_bootstr()
            # do stuff
            self.event_manager.bootstr_received.clear()

        # give data to the p2p
        if self.event_manager.height_request.isSet():
            p2p_api.send_height(my_height)
            # do stuff
            self.event_manager.height_request.clear()

        if self.event_manager.block_request.isSet():
            # returns list of block numbers
            number_list = p2p_api.get_requ_block_numbers()
            for number in number_list:
                p2p_api.send_block(number, the_block_to_number)
            # do stuff
            self.event_manager.block_request.clear()

        if self.event_manager.tx_request.isSet():
            # do stuff
            self.event_manager.tx_request.clear()

        if self.event_manager.tx_pool_request.isSet():
            p2p_api.send_pool(self.pool.string())
            self.event_manager.tx_pool_request.clear()

        if self.event_manager.bootstr_request.isSet():
            from_block_number, to_block_number, reciever = p2p_api.get_requ_bootstr_numbers()
            temp = []
            # fill temp with the blocks from and to
            p2p_api.send_bootstr(reciever, temp)
            # do stuff
            self.event_manager.bootstr_request.clear()

        if self.event_manager.connection_lost.isSet():
            # reconnect maybe ?
            # do stuff
            self.event_manager.connection_lost.clear()

        if self.event_manager.error.isSet():
            loggerutil.error(p2p_api.get_error_message())
            # shut down the client after logging the error
            p2p_api.stop_peer(self.peer)
            return True

        return False

    def send_event_manager(self):
        """returns event_manager object of client"""
        p2p_api.em(self.event_manager)


