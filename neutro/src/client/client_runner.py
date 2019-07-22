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

datastructure
    -the client keeps some of the current chain in memory (at least till block -7)
    -it keeps it in a dictionary of lists of blocks, with the key beeing the height
        -dict(height:List[MainBlock])

"""

import threading
from neutro.src.chain import *
from neutro.src.chain.main_block import MainBlock
from neutro.src.chain.shard_block import ShardBlock
from neutro.src.chain.vote import Vote
from neutro.src.chain.transaction import Transaction
from neutro.src.chain.voting_token_transaction import VotingTokenTransaction
from neutro.src.util import loggerutil
from neutro.src.util.wallet import Wallet
from neutro.src.database import wallet_database
from neutro.src.database import block_database
from neutro.src.client.vote_pool import VotePool
from neutro.src.client.block_pool import BlockPool
from neutro.src.client.transaction_pool import TransactionPool
from neutro.src.p2p.p2p_api import P2P_API
from neutro.src.p2p.peer import Peer
from neutro.src.config.config_util import get_peer_list
import time
from enum import Enum
from .event_manager import EventManager


class State(Enum):
    DEFAULT = -1
    UPDATING = 0
    WAITING = 1
    MINING = 2


class Client(threading.Thread):
    """this class does all the previously described tasks"""

    fields = [
        ("wallet", Wallet),
        ("p2p_api", P2P_API),

        ("vote_pool", VotePool),
        ("tx_pool", TransactionPool),
        ("vtx_pool", TransactionPool),
        ("main_block_pool", BlockPool),
        ("shard_block_pool", BlockPool),

        ("event_manager", EventManager),
        ("event_stop", threading.Event),

        ("state", State),

        ("current_difficulty", str),

        ("current_height", int),
        ("stable_height", int),
        ("last_fork_height", int)
    ]

    def __init__(self):
        threading.Thread.__init__(self)
        #self.wallet = wallet_database.load_wallet()
        self.p2p_api = P2P_API()

        self.vote_pool = VotePool()
        self.tx_pool = TransactionPool()
        self.vtx_pool = TransactionPool()
        self.main_block_pool = BlockPool()
        self.shard_block_pool = BlockPool()

        self.event_manager = self.p2p_api.event_mg
        self.stop = threading.Event()

        self.state = State.DEFAULT

        # self.start()

    def connect(self, connect_to_peer: Peer=None):
        """
        lets you connect to a peer 
        or connects you to the list of peers in the config file
        """
        if connect_to_peer:
            self.p2p_api.connect(connect_to_peer)
        else:
            for peer_to_connect_to in get_peer_list():
                self.p2p_api.connect(peer_to_connect_to)

    def run(self):
        """method required by threading to start a thread"""
        loggerutil.info("client update started")
        self.update()
        loggerutil.info("client update complete")

        loggerutil.info("client started")
        self.loop()
        loggerutil.info("client stopped")

    def update(self):
        """updates a client to the current state of the network"""
        self.state = State.UPDATING

        # blocking calls
        self.current_difficulty = p2p_api.get_current_difficulty()
        self.current_height = p2p_api.get_current_height()
        # get last stable chain height
        # (stable means no forks and 7 confirmations)
        self.stable_height = block_database.get_stable_height()

        # blocking call, connects this peer to other known peers
        self.connect()

        loggerutil.debug("client connected")

        # blocking call
        client_net = self.p2p_api.list_peers_in_net(self.peer)
        loggerutil.debug(
            "Client with host {0} - Current state of the net {1}".format(self.peer_host, client_net))

        # init all the pools

        # blocking call only returns list of missing blocks
        self.p2p_api.update_chain(
            self.my_height, self.current_height)

        # go over all the blocks that came along since this client was last
        # online
        for b in block_list:
            self.main_block_pool.add_block(b)

        # not blocking call because peers could have different versions of the
        # pool, makes the p2p api request blocks from different peers and send
        # them all to this client
        self.p2p_api.update_block_pool()

        # not blocking call because peers could have different versions of the
        # pool, makes the p2p api request blocks from different peers and send
        # them all to this client
        self.p2p_api.update_tx_pool()

        # here we should be finished with the update of the client (except for
        # all blocks in pool and tx in pool)

    def loop(self):
        """this method loops for ever until it is stopped by force or with the "stop" event"""
        while True:
            if self.stop.isSet():
                loggerutil.debug("shutting down client")
                break
            if self.manage_events():
                loggerutil.debug("shutting down client due to an error")
                break

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
            loggerutil.debug(
                "block received event is triggered by: {0}:".format(self.peer_host))
            loggerutil.debug("Block string: {0}".format(block))
            self.event_manager.block_received.clear()
            handle_new_block(block)

        if self.event_manager.tx_received.isSet():
            tx = self.p2p_api.get_recv_tx(self.peer_host)
            loggerutil.debug(
                "transaction received event is triggered by: {0}:".format(self.peer_host))
            loggerutil.debug("Tx string: {0}".format(tx))
            self.event_manager.tx_received.clear()
            handle_new_tx(tx)

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
            # check if the highest blockchain of a client is the same as from
            # the list
            if len(self.chain) == last_num_from_list:
                # send the blocks that are missing from smaller chains
                for number in number_list:
                    self.p2p_api.send_block(number, self.chain[number - 1])
            # do stuff
            self.event_manager.block_request.clear()

        if self.event_manager.tx_request.isSet():
            # do stuff
            self.event_manager.tx_request.clear()

        if self.event_manager.tx_pool_request.isSet():
            self.p2p_api.send_pool(self.pool.string())
            self.event_manager.tx_pool_request.clear()

        if self.event_manager.bootstr_request.isSet():
            from_block_number, to_block_number, receiver = self.p2p_api.get_requ_bootstr_numbers()
            temp = []
            # fill temp with the blocks from and to
            self.p2p_api.send_bootstr(receiver, temp)
            # do stuff
            self.event_manager.bootstr_request.clear()

        if self.event_manager.connection_lost.isSet():
            # reconnect maybe ? (probably not till milestone 4)
            # do stuff
            self.event_manager.connection_lost.clear()

        if self.event_manager.error.isSet():
            loggerutil.debug("shutdown event is triggered")
            # loggerutil.error(self.p2p_api.get_error_message())
            # shut down the client after logging the error
            self.p2p_api.stop_peer_thread(self.peer)
            return True

        return False

    def handle_new_block(self, block):
        """handles blocks received from the p2p network"""
        if isinstance(block, MainBlock):
            handle_new_main_block(block)
        elif isinstance(block, ShardBlock):
            handle_new_shard_block(block)
        else:
            loggerutil.error(
                "received block that was neither main nor shard block")

    def handle_new_main_block(self, main_block: MainBlock):
        self.main_block_pool.add_block(main_block)
        loggerutil.debug("got new main_block: " + main_block.str())

    def handle_new_shard_block(self, shard_block: ShardBlock):
        self.shard_block_pool.add_block(shard_block)
        loggerutil.debug("got new shard_block: " + shard_block.str())

    def handle_new_tx(self, tx):
        """handles tx received from the p2p network"""
        if isinstance(tx, Transaction):
            handle_new_transaction(tx)
        elif isinstance(tx, VotingTokenTransaction):
            handle_new_vtx(tx)
        else:
            loggerutil.error("received tx that was neither tx nor vtx")

    def handle_new_transaction(self, tx: Transaction):
        self.tx_pool.add_transaction(tx)
        loggerutil.debug("got new tx: " + tx.str())

    def handle_new_vtx(self, vtx: VotingTokenTransaction):
        self.vtx_pool.add_transaction(tx)
        loggerutil.debug("got new vtx: " + vtx.str())
