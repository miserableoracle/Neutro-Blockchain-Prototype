import os
import shutil
from pathlib import Path

from src.util import loggerutil


def save_block(height: int, block_json_string: str, block_hash: str):
    """saves a block and updates the list of height:hash for resolution of height from hash"""
    block_path = str(Path(__file__).parent.parent.parent) + \
        "/.data/blocks/"
    Path(block_path).mkdir(parents=True, exist_ok=True)
    # if there is a dicionary for height:block_hash
    if os.path.isfile("{0}/hash.dictionary".format(block_path)):
        # check if there is already a block for given height
        if "{}:".format(height) in open("{0}/hash.dictionary".format(block_path)).read():
            loggerutil.error("could not save block " + block_json_string +
                             " because there is already a block at height " + str(height))
            raise ValueError(
                "there is already a block at height " + str(height))

    # update the dicionary for height:hash
    with open("{0}/hash.dictionary".format(block_path), "a") as hash_file:
        print("{0}:{1}".format(str(height), block_hash), file=hash_file)
    # save the block as json
    with open("{0}/{1}.block".format(block_path, str(height)), "w") as block_file:
        print("{}".format(block_json_string), file=block_file)


def load_block_by_height(height: int) -> str:
    """loads a block by height/number and returns the json-string of this block"""
    block_path = str(Path(__file__).parent.parent.parent) + \
        "/.data/blocks/" + str(height) + ".block"
    if not os.path.isfile(block_path):
        loggerutil.error("could not load block for height " + str(height))
        raise ValueError("there is no block at height " + str(height))
    # read the block from file
    with open("{0}".format(block_path), "r") as block_file:
        return block_file.read()


def load_block_by_hash(block_hash: str) -> str:
    """loads the height/number of a block from the dicionary, returns load_block_by_height(said height)"""
    hash_path = str(Path(__file__).parent.parent.parent) + \
        "/.data/blocks/hash.dicionary"
    if not os.path.isfile(hash_path):
        loggerutil.error("could not load the block_hash database")
        raise ValueError("there is no block_hash database")
    # open the block_hash database
    with open(hash_path, "w") as hash_file:
        for line in hash_file:
            # read all lines and compare to block_hash
            if line.split(":")[1] == block_hash:
                # if found return block for height
                return load_block_by_height(int(line.split(":")[0]))
        loggerutil.error("could not load block with hash " + block_hash)
        raise ValueError("there is no block with hash " +
                         block_hash + " in block database")


def remove_database(height: int):
    """
    removes all blocks, this is just for testing purpouses
    WARNING: use with care, it will delete the complete blockchain!! 
    """
    block_path = str(Path(__file__).parent.parent.parent) + \
        "/.data/blocks/"
    shutil.rmtree(wallet_path)
