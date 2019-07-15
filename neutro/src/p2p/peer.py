from atomic_p2p.peer import Peer as AtomicP2PPeer

from .neutro_handler import NeutroHandler
from neutro.src.util import loggerutil


class Peer(AtomicP2PPeer):
    """neutro peer that registers our neutro handler with a callback functionality"""
    def __init__(self, host, name, role, cert, _hash):
        super().__init__(
            host=host, name=name, role=role, cert=cert, _hash=_hash)

    def process_sync_data(self, data):
        print("callback {}".format(data))
        return data

    def _register_handler(self) -> None:
        # calls the original method implementation
        super()._register_handler()
        # adds NeutroHandler to current handlers of
        installing_handler = [
            NeutroHandler(self, self.process_sync_data)
        ]
        for each in installing_handler:
            self.pkt_handlers[each.pkt_type] = each
