from neutro.src.cli.commands.base import Base
from neutro.src.chain.transaction import from_json_string
from neutro.src.database import wallet_database


class TransactionCommand(Base):

    def run(self):
        if self.options["get"]:
            print("todo")
        elif self.options["publish"]:
            print("todo")
        elif self.options["verify"]:
            try:
                from_json_string(self.options["<json_string>"]).verify()
                print(True)
            except:
                print(False)
        elif self.options["sign"]:
            w = wallet_database.load_wallet()
            t = from_json_string(self.options["<json_string>"])
            t.sender_address = w.get_address()
            w.sign_transaction(t)
            wallet_database.save_nonce(w.get_nonce())
            print("Hash:\n" + t.hash())
            print("Raw:\n" + t.string())
