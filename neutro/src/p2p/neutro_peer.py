from atomic_p2p.peer import Peer
from neutro.src.p2p.neutro_handler import NeutroHandler
from neutro.src.util import loggerutil


class NeutroPeer(Peer):

    def __init__(self, host, name, role, cert, _hash):
        super(NeutroPeer, self).__init__(
            host=host, name=name, role=role, cert=cert, _hash=_hash)

    def _register_handler(self):
        super(NeutroPeer, self)._register_handler()
        installing_handlers = [
            NeutroHandler(self)
        ]
        for each in installing_handlers:
            self.pkt_handlers[type(each).pkt_type] = each
