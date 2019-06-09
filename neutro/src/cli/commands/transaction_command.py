from neutro.src.client.commands.base import Base


class TransactionCommand(Base):

    def run(self):
        print("transaction")
