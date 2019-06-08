"""
this class implements a very rudamentary version of proof-of-work.
The Neutro Consensus will be implemented in milestone 3
"""
import time
import threading
from src.util import loggerutil
from src.util import hashutil
from src.util import stringutil
from src.chain.block import Block


class Pow(threading.Thread):

    def __init__(self, block: Block):
        threading.Thread.__init__(self)
        self.block = block
        self.stop = threading.Event()
        self.stop_external = threading.Event()

    def run(self):
        if not self.block:
            return

        nonce = self.block.nonce
        difficulty = self.block.difficulty

        self.start_time = time.time()
        while True:
            if stringutil.hex_string_to_int(self.block.hash()) <= stringutil.hex_string_to_int(difficulty):
                self.stop.set()
            else:
                nonce = stringutil.int_to_hex_string(
                    stringutil.hex_string_to_int(nonce) + 1, 16)
                self.block.nonce = nonce
            if self.stop.isSet():
                break
        self.end_time = time.time()
        if self.stop_external.isSet():
            loggerutil.debug("stopped mining block with difficulty "
                             + self.block.difficulty + " after "
                             + str(self.end_time - self.start_time) + " seconds")
        else:
            loggerutil.debug("mined block with difficulty "
                             + self.block.difficulty + " and hash "
                             + self.block.hash() + " in "
                             + str(self.end_time - self.start_time) + " seconds")

    def get_mined_block(self):
        if not self.stop.isSet():
            raise PowNotFinishedWarning()
        return self.block

    def interrupt(self):
        self.stop.set()
        self.stop_external.set()
        raise PowNotFinishedWarning()

    def isInterrupted(self):
        return self.stop.isSet()


class PowNotFinishedWarning(RuntimeWarning):
    """used to warn that mining is not finished"""
    pass
