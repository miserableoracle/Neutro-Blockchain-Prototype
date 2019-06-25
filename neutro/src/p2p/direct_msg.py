from neutro.src.p2p.p2p_api import send_transaction_direct
from neutro.src.p2p.p2p_api import send_block_direct
import time

#import socket
#socket.SO_REUSEPORT = 15


def direct_messaging_tx():
    send_tx_direct = send_transaction_direct()
    json_string_transaction = send_tx_direct['tx_string']
    from_peer = send_tx_direct['from_peer']
    to_peer = send_tx_direct['to_peer']

    # sends a transaction from a peer to another
    core = from_peer
    switch = to_peer

    # Starts the thread’s activities
    core.start()
    switch.start()

    # Sends a join request to core peer
    switch.onProcess(['join', '127.0.0.1:{}'.format(core.server_info.host[1])])
    time.sleep(5)

    # Send a transaction message from one peer to the other
    switch.onProcess(['send', '127.0.0.1:{}'.format(core.server_info.host[1]), json_string_transaction])
    time.sleep(5)


def direct_messaging_block():
    # sends a block from a peer to another

    send_b_direct = send_block_direct()
    json_string_block = send_b_direct['block_string']
    from_peer = send_b_direct['from_peer']
    to_peer = send_b_direct['to_peer']

    core = from_peer
    switch = to_peer

    # Starts the thread’s activities
    core.start()
    switch.start()

    # Sends a join request to core peer
    switch.onProcess(['join', '127.0.0.1:{}'.format(core.server_info.host[1])])
    time.sleep(5)

    # Send a block message from one peer to the other
    switch.onProcess(['send', '127.0.0.1:{}'.format(core.server_info.host[1]), json_string_block])
    time.sleep(5)


direct_messaging_tx()
direct_messaging_block()
