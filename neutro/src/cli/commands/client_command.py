from neutro.src.cli.commands.base import Base


class ClientCommand(Base):

    def run(self):
        print("client")
