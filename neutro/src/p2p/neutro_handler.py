from atomic_p2p.utils.communication import Handler, Packet
from neutro.src.util import loggerutil

class NeutroHandler(Handler):
    '''handles the packet's sending and receiving'''
    pkt_type = "neutro_pkt"

    def __init__(self, peer, callback):
        super(NeutroHandler, self).__init__(
            peer=peer, pkt_type=type(self).pkt_type)
        self.callback = callback

    def on_send_pkt(self, target, msg):

        data = {
            "msg": msg
        }

        self.peer.logger.info("The packet is being sent")
        return Packet(dst=target, src=self.peer.server_info.host,
                      _hash=self.peer._hash, _type=type(self).pkt_type, _data=
                      data)

    def on_recv_pkt(self, src, pkt, conn):
        data = pkt.data
        self.peer.logger.info("The packet has been received")
        self.peer.logger.info("src: {}, pkt: {}".format(src, pkt))
        self.callback(pkt.data)


