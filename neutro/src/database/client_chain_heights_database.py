import os
from pathlib import Path
from typing import List
import ast
from neutro.src.util import loggerutil


def store_client_chain_height(client_host: str, client_height):
    """stores the height of the chain"""
    client_chain_height_path = str(Path(__file__).parent.parent.parent) + \
        "/.data/client_chain_height/"
    print(client_chain_height_path)
    Path(client_chain_height_path).mkdir(parents=True, exist_ok=True)
    with open("{0}/{1}".format(client_chain_height_path, client_host), "w") as client_chain_height_file:
        print("{}".format(client_height), file=client_chain_height_file)


def get_client_chain_height(client_host: str):
    """gets the directly connected nodes of a peer"""
    client_chain_height_path = str(Path(__file__).parent.parent.parent) + \
                     "/.data/client_chain_height/"
    #if not os.path.isfile(client_chain_height_path):
    #    return 0
    try:
        with open("{0}/{1}".format(client_chain_height_path, client_host), "r") as client_chain_height_file:
            return ast.literal_eval(client_chain_height_file.read())
    except:
        return 1
