"""this class represents the wallet command"""
from neutro.src.cli.commands.base import Base

from neutro.src.util import wallet
from neutro.src.database import wallet_database


class WalletCommand(Base):

    def run(self):
        if self.options["import"]:
            print("import wallet not supported for now")
        elif self.options["export"]:
            print("export wallet not supported for now")
        elif self.options["generate_wallet"]:
            self.gen_wallet()
        elif self.options["get_address"]:
            print(wallet_database.get_address())
        elif self.options["get_nonce"]:
            print(wallet_database.get_nonce())

    def gen_wallet(self):
        # we only want to generate a new wallet if there is none
        # (todo make it better, if input throws an exception the old wallet is gone)
        try:
            wallet_database.load_wallet()
            y = input(
                "There is already a wallet with address:\n " + wallet_database.get_address() +
                "\nGenerating a new wallet would override Your old wallet.\n\n"
                + "You would loose access to the old wallet.\n\nAre You Sure? (y/N)")
            if y == "y" or y == "Y":
                wallet_database.save_wallet(wallet.generate_new_wallet())
                print("\nGenerated wallet with address:\n" +
                      wallet_database.get_address())
        except:
            wallet_database.save_wallet(wallet.generate_new_wallet())
            print("generated wallet with address:" +
                  wallet_database.get_address())
            # todo save old wallet in temp or sth
