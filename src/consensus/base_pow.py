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
    """this class dose basic pow work on a seperate thread"""

    def __init__(self, block: Block):
        threading.Thread.__init__(self)
        self.block = block
        self.stop = threading.Event()
        self.stop_external = threading.Event()

    def run(self):
        if not self.block:
            return
        # start with the nonce already in the block. this should enable
        # multiple Threads to work on the same block with different starting
        # points
        nonce = self.block.nonce
        difficulty = self.block.difficulty
        self.start_time = time.time()
        while True:
            # test if difficulty target is reached
            if stringutil.hex_string_to_int(self.block.hash()) <= stringutil.hex_string_to_int(difficulty):
                self.stop.set()
            else:
                # count the nonce up
                nonce = stringutil.int_to_hex_string(
                    stringutil.hex_string_to_int(nonce) + 1, 16)
                self.block.nonce = nonce
            # look for external interruption
            if self.stop.isSet():
                break
        # capture the time it took to mine
        self.end_time = time.time()
        # log everything
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
        """returns the mined block"""
        if not self.stop.isSet():
            raise PowNotFinishedWarning()
        return self.block

    def interrupt(self):
        """stops mining"""
        self.stop.set()
        self.stop_external.set()
        raise PowNotFinishedWarning()

    def isInterrupted(self):
        """returns if this thread is beeing stopped"""
        return self.stop.isSet()


class PowNotFinishedWarning(RuntimeWarning):
    """used to warn that mining is not finished"""
    pass
