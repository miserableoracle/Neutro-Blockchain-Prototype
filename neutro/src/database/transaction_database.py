from pathlib import Path

from neutro.src.util import loggerutil


key_path = str(Path(__file__).parent.parent.parent) + \
    "/.data/txs/" + address
