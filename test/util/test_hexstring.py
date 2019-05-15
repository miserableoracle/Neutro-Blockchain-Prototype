from src.util.hexstring import Hexstring

# Test1: test a string value against the corresponding hash value of it
value = "0x0123456789abcdef"
hex_value = '307830313233343536373839616263646566'

# create an object of Hexstring class
hex_string = Hexstring()
# string to byte
value_encoded_byte = hex_string.str_encode(value)
# byte to hex string
hex_string_value = hex_string.encode_hex(value_encoded_byte)

# Assertion
assert hex_value == hex_string_value
