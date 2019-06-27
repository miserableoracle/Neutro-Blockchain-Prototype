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
    -boradcast and send blocks and tx to other nodes
    -recieve requests (event manager)
"""

import time
import threading
from neutro.src.util import loggerutil
from neutro.src.database import wallet_database
from neutro.src.client.event_manager import EventManager
from neutro.src.client.transaction_pool import Pool
from neutro.src.p2p import p2p_api


class Client(threading.Thread):
    """this class dose all the previously described tasks"""

    def __init__(self, block: Block):
        threading.Thread.__init__(self)
        self.stop = threading.Event()
        self.wallet = wallet_database.load_wallet()
        self.event_manager = EventManager()
        self.peer = p2p_api.create_a_peer(
            role="myself", name=self.wallet.get_address(), host=("0.0.0.0", 8000))
        self.pool = Pool()
        self.start()

    def run(self):
        loggerutil.debug("client started")

        # blocking call, connects this peer to other known peers
        p2p_api.connect(self.peer)
        loggerutil.debug("client connected")

        # blocking call, returns the latest block number
        current_height = p2p_api.get_current_height()
        my_current_heigth = block_database.get_current_height()
        if current_height > my_current_heigth:
            # blocking call, returns a list of blocks from x to y (my heigth,
            # network height)
            bootstrap = p2p_api.get_bootstrap(
                my_current_heigth, current_height)
            for block in bootstrap:
                if not self.validate_block(block):
                    loggerutil.error("published block: " +
                                     block + " is not valid. Exiting!")
                    return
                block_database.save_block()
        elif current_height < my_current_heigth:
            loggerutil.error(
                "local chain is longer than network chain at startup, this should never happen!!")

        # blocking call, returns the current tx pool as a list of transactions
        tx_pool_list = p2p_api.get_tx_pool()
        for tx in tx_pool_list:
            if not self.validate_tx(tx):
                loggerutil.error("pooled tx: " + tx +
                                 " is not valid. Exiting!")
            self.pool.add_transaction(tx)

        loggerutil.debug("client synched")

        self.loop()

    def loop(self):
        """this method loops for ever until it is stopped by force or with the "stop" event"""
        while True:
            if self.stop.isSet():
                loggerutil.debug("shutting down client")
                break
            if self.manage_events():
                loggerutil.debug("shuttind down client due to an error")
                break

            # start of the pow

    def validate_block(block: str) -> bool:
        """a lot of steps to validate if a block is correct"""
        return True

    def validate_tx(tx: str) -> bool:
        """a lot of steps to validate if a tx is correct"""
        return True

    def manage_events() -> bool:
        """
        Manages all functionality that has to be asynchronous. 
        All these events can be set by the p2p api, the client then handles these events in its own thread

        returns a bool that is only True if the client needs to be shut down in case of an error
        """
        if self.event_manager.block_received.isSet():
            pass
        elif self.event_manager.tx_received.isSet():
            pass
        elif self.event_manager.height_request.isSet():
            pass
        elif self.event_manager.block_request.isSet():
            pass
        elif self.event_manager.tx_request.isSet():
            pass
        elif self.event_manager.tx_pool_request.isSet():
            pass
        elif self.event_manager.bootstr_request.isSet():
            pass
        elif self.event_manager.error.isSet():
            pass
        elif self.event_manager.connection_lost.isSet():
            pass
        else
            return False
