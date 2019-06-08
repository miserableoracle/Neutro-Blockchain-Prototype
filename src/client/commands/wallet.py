"""this class represents the generate_wallet command"""
from src.client.commands.base import Base
from src.util.wallet import Wallet


class WalletCommand(Base):

    def run(self):
        print("HI")
        print(self.options)
