"""
neutro.

Usage:
    neutro -h | --help
    neutro -v | --version
    neutro hello
    neutro wallet import <path_to_key_file>
    neutro wallet export <path>
    neutro wallet get address
    neutro start
    neutro stop
    neutro add peer <peer_address>
    neutro block get <no> | <hash>
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
from . import __version__ as VERSION
from src.util import loggerutil

project_root = str(Path(__file__).parent.parent.parent)
os.chdir(project_root)


def main():
    """main command line interface entry point"""
    import src.client.commands
    options = docopt(__doc__, version=VERSION)
    # here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (k, v) in options.items():
        if hasattr(src.client.commands, k) and v:
            module = getattr(src.client.commands, k)
            commands = getmembers(module, isclass)
            command = [c for c in commands
                       if c[0].lower() == k.lower() + "command"][0][1]
            command = command(options)
            command.run()
            loggerutil.debug("CLI: run command " + str(command))
