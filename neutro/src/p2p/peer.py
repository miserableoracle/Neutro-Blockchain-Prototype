from atomic_p2p.peer import Peer as AtomicP2PPeer

from .neutro_handler import NeutroHandler
from neutro.src.util import loggerutil
import os
from os import getcwd
from os.path import join
from atomic_p2p.utils.security import self_hash as sh, create_self_signed_cert


class Peer(AtomicP2PPeer):
    """neutro peer that registers our neutro handler with a callback functionality"""
    def __init__(self, host):
        self_hash = sh(join(os.getcwd()))

        # Peers must have the same certificate
        cert = create_self_signed_cert(getcwd(), 'data/certificate.pem', 'data/private.key')
        super().__init__(
            host=host, name="node"+host[0]+"-"+str(host[1]), role="neutro_peer", cert=cert, _hash=self_hash)

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
