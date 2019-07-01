from pathlib import Path
from typing import List
import ast
from neutro.src.util import loggerutil


def store_messages(src, packet, message):
    """stores a peer with its respective list of neighbors"""
    messages_path = str(Path(__file__).parent.parent.parent) + \
        "/.data/messages/"
    print(messages_path)
    Path(messages_path).mkdir(parents=True, exist_ok=True)
    with open("{0}/{1}".format(messages_path, src), "w") as messages_file:
        print("{0}/{1}".format(packet, message), file=messages_file)


def ges_messages(src):
    """gets the directly connected nodes of a peer"""
    messages_path = str(Path(__file__).parent.parent.parent) + \
                     "/.data/messages/"
    with open("{0}/{1}".format(messages_path, src), "r") as messages_file:
        return ast.literal_eval(messages_file.read())

