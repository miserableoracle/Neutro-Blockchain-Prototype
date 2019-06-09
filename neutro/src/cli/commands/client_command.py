from neutro.src.client.commands.base import Base


class ClientCommand(Base):

    def run(self):
        print("client")
