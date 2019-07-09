from pathlib import Path
from typing import List
import ast
from neutro.src.util import loggerutil


def store_messages(src, packet, message):
    """stores a message sent from a peer source"""
    messages_path = str(Path(__file__).parent.parent.parent) + \
        "/.data/messages/"
    Path(messages_path).mkdir(parents=True, exist_ok=True)
    with open("{0}/{1}".format(messages_path, src), "w") as messages_file:
        print("{0}".format(message['msg']), file=messages_file)


def store_messages_details(src, packet, message):
    """stores a message and packet delivery details from a peer source"""
    messages_path = str(Path(__file__).parent.parent.parent) + \
        "/.data/messages_details/"
    Path(messages_path).mkdir(parents=True, exist_ok=True)
    with open("{0}/{1}".format(messages_path, src), "w") as messages_file:
        print("{0}/{1}".format(packet, message), file=messages_file)


def get_messages(src):
    """gets the directly connected nodes of a peer"""
    messages_path = str(Path(__file__).parent.parent.parent) + \
                     "/.data/messages/"
    try:
        with open("{0}/{1}".format(messages_path, src), "r") as messages_file:
            return ast.literal_eval(messages_file.read())
    except FileNotFoundError:
        print("There is no message stored for {0}".format(src))

