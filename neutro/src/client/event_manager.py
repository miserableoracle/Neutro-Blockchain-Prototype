import threading
from threading import Event


class EventManager():
    __init__(self):
        self.block_received = Event()
        self.tx_received = Event()
        self.bootstr_received = Event()
        self.block_request = Event()
        self.tx_request = Event()
        self.bootstr_request = Event()
        self.error = Event()
        self.connection_lost = Event()
