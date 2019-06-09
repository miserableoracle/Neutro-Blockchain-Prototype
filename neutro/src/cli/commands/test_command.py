"""The hello command."""
from json import dumps

from neutro.src.cli.commands.base import Base


class TestCommand(Base):
    """Say hello, world!"""

    def run(self):
        print('Hello, world!')
        print('You supplied the following options:', dumps(
            self.options, indent=2, sort_keys=True))
