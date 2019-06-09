"""
neutro.

Usage:
    neutro -h | --help
    neutro -v | --version
    neutro test
    neutro wallet import <path_to_wallet>
    neutro wallet export <path>
    neutro wallet generate_wallet
    neutro wallet get_address
    neutro wallet get_nonce
    neutro client start
    neutro client stop
    neutro client add_peer <peer_address>
    neutro block get_by_hash
    neutro block get_by_no
    neutro transaction get <hash>
    neutro transaction publish <json_string>
    neutro transaction verify <json_string>
    neutro transaction sign <json_string> [<path_to_key_file>]

Options:
    -h --help
    -v --version
"""
import os
from pathlib import Path
from docopt import docopt
from inspect import getmembers, isclass
from neutro.src.client import __version__ as VERSION
from neutro.src.util import loggerutil

from neutro.src.client.commands.test_command import TestCommand
from neutro.src.client.commands.wallet_command import WalletCommand
from neutro.src.client.commands.block_command import BlockCommand
from neutro.src.client.commands.transaction_command import TransactionCommand
from neutro.src.client.commands.client_command import ClientCommand

# make sure the interpreter finds all the packages
project_root = str(Path(__file__).parent.parent.parent)


def main():
    options = docopt(__doc__, version=VERSION)
    loggerutil.debug("CLI: run command with options: " +
                     str(options).replace("\n", ""))
    # map all the commands to the classes
    if options["test"]:
        TestCommand(options).run()
    elif options["wallet"]:
        WalletCommand(options).run()
    elif options["transaction"]:
        TransactionCommand(options).run()
    elif options["block"]:
        BlockCommand(options).run()
    elif options["client"]:
        ClientCommand(options).run()
