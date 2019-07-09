import threading
from threading import Event
from neutro.src.util import loggerutil


class EventManager():
    """this class is just a holder object for all the events the p2p thread needs the client to know"""

    def __init__(self):
        # get data from the p2p
        self.block_received = Event()
        self.tx_received = Event()
        self.tx_pool_received = Event()
        self.bootstr_received = Event()
        # give data to the p2p
        self.height_request = Event()
        self.block_request = Event()
        self.tx_request = Event()
        self.tx_pool_request = Event()
        self.bootstr_request = Event()
        # handle errors
        self.connection_lost = Event()
        self.error = Event()

