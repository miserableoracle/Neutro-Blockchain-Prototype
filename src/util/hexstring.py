import codecs


class Hexstring(object):
    """An object for hex string data"""

    def __init__(self, value=None):
        if value is None:
            pass
        elif self.is_text(value) is True:
            self.encode_hex(self.str_encode(value))

    # define string types
    string_types = (str, bytes, bytearray)

    def is_string(self, variable) -> bool:
        # checks if a type of variable is a string (including unicode)
        return isinstance(variable, self.string_types)

    def is_text(self, value) -> bool:
        # checks if a type is string
        return isinstance(value, str)

    def str_encode(self, n: str) -> bytes:
        # encodes a string to default Utf-8 Encoding
        if not self.is_text(n):
            raise TypeError("Value must be an instance of str")
        return n.encode('utf-8')

    def encode_hex(self, value) -> str:
        # encodes a value of any type of string to a hex string
        if not self.is_string(value):
            raise TypeError("Value must be an instance of str or unicode")
        # bytes to hex bytes encoding
        hex_enc = codecs.encode(value, "hex")

        # hex bytes to hex string
        return hex_enc.decode("ascii")

    def decode_hex(self, value: str) -> bytes:
        # decodes a string to hex bytes
        if not self.is_text(value):
            raise TypeError("Value must be an instance of str")

        return codecs.decode(value, "hex")


HexString = Hexstring()

