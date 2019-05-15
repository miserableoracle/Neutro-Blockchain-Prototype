"""utils for managing crypto"""


def generate_priate_key() -> str:
    private_key = RSA.generate(1024)
    public_key = private_key.publickey()
    print(private_key.exportKey(format='PEM'))
    print(public_key.exportKey(format='PEM'))


def private_to_public(private_key: bytes) -> str:
    return private_key.publickey()


def sign(message):
    """
    Sign a message
    """
    hashed = SHA.new(message.encode('utf8'))
    return binascii.hexlify(self.signer.sign(hashed)).decode('ascii')
