from pathlib import Path
from typing import List
import ast


def store_neighbors(peer_name: str, peer_neighbors: List[str]):
    """stores a peer with its respective list of neighbors"""
    neighbors_path = str(Path(__file__).parent.parent.parent) + \
        "/.data/neighbors/"
    print(neighbors_path)
    Path(neighbors_path).mkdir(parents=True, exist_ok=True)
    with open("{0}/{1}".format(neighbors_path, peer_name), "w") as neighbors_file:
        print("{}".format(peer_neighbors), file=neighbors_file)


def get_neighbors(peer_name: str):
    """gets the directly connected nodes of a peer"""
    neighbors_path = str(Path(__file__).parent.parent.parent) + \
                     "/.data/neighbors/"
    with open("{0}/{1}".format(neighbors_path, peer_name), "r") as neighbors_file:
        return ast.literal_eval(neighbors_file.read())

