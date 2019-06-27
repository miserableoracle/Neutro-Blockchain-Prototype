import threading
from threading import Event
from neutro.src.util import loggerutil


class EventManager():
	"""this class is just a holder object for all the events the p2p thread needs the client to know"""
    __init__(self):
        self.block_received = Event()
        self.tx_received = Event()
        self.height_request = Event()
        self.block_request = Event()
        self.tx_request = Event()
        self.tx_pool_request = Event()
        self.bootstr_request = Event()
        self.error = Event()
        self.connection_lost = Event()
