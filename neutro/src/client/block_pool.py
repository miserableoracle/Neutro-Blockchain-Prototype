"""
implements a block pool based on a
dict(height:List[block])
"""
from neutro.src.util import loggerutil
from neutro.src.chain.main_block import MainBlock
from neutro.src.chain.shard_block import ShardBlock


class BlockPool(object):
    """docstring for BlockPool"""

    def __init__(self):
        self.blocks = {}
        self.current_height = 0

    def get_block_dict(self) -> dict:
        """returns the dict of blocks"""
        return self.blocks

    def get_current_height(self) -> int:
        """returns the current height of the chain"""
        return self.current_height

    def add(self, block):
        """adds a block to the pool, also updating the current height"""
        
        try:
            self.blocks[block.height]
        except:
            self.blocks[block.height] = [block]
            if self.current_height < block.height:
                self.current_height = block.height
            return

        if not block.hash() in [b.hash() for b in self.blocks[block.height]]:
            self.blocks[block.height].append(block)
            loggerutil.debug("fork detected for height:" + str(block.height) +
                             "block candidats:" + str(self.blocks[block.height]))
            if self.current_height < block.height:
                self.current_height = block.height

    def remove(self, block):
        """removes a block from the pool"""
        try:
            self.blocks[block.height]
        except:
            raise ValueError("cant remove block: " + str(block))

        removed = False
        for b in self.blocks[block.height]:
            # only delete the one with equal hash
            if b.hash() == block.hash():
                self.blocks[block.height].remove(b)
                removed = True
            if self.blocks[block.height] == []:
                self.blocks.pop(block.height)

        if not removed:
            raise ValueError("cant remove block: " + str(block))

    def get_blocks_by_height(self, height: int):
        """returns a list of blocks for the give height"""
        try:
            return self.blocks[height]
        except:
            return None
