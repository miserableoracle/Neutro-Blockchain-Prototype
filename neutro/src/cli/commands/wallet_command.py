"""this class represents the generate_wallet command"""
from neutro.src.client.commands.base import Base

from neutro.src.util import wallet
from neutro.src.database import wallet_database


class WalletCommand(Base):

    def run(self):
        if self.options["import"]:
            print("import wallet not supported for now")
        elif self.options["export"]:
            print("export wallet not supported for now")
        elif self.options["generate_wallet"]:
            wallet_database.save_wallet(wallet.generate_new_wallet())
            print("generated wallet with address:" +
                  wallet_database.get_address())
            # todo save old wallet in temp or sth
        elif self.options["get_address"]:
            print(wallet_database.get_address())
        elif self.options["get_nonce"]:
            print(wallet_database.get_nonce())
