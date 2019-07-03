"""singing and verifying messages and transactions"""
import base58
import ecdsa
import binascii


def key_to_address(public_key: ecdsa.VerifyingKey) -> str:
    """returns a b58 encoded version of the public_key"""
    return str(base58.b58encode(public_key.to_string()))[2:-1]


def address_to_key(address: str) -> ecdsa.VerifyingKey:
    """returns a public key, decoded from the address"""
    return ecdsa.VerifyingKey.from_string(bytes.fromhex(binascii.hexlify(
        base58.b58decode(address)).decode('utf-8')), curve=ecdsa.SECP256k1)


def generate_key() -> ecdsa.SigningKey:
    """generates and returns a new private_key"""
    return ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)


def sign_message(private_key: ecdsa.SigningKey, message: str) -> str:
    """returns a signature for a given message"""
    signature = private_key.sign(bytes(message, "utf-8"))
    return str(binascii.hexlify(signature))[2:-1]


def verify_message(public_key: ecdsa.VerifyingKey, message: str, _signature: str) -> bool:
    """verifies message and signature against public_key"""
    signature = binascii.unhexlify(_signature)
    return public_key.verify(signature, bytes(message, "utf-8"))


def get_vote_sig(private_key: ecdsa.SigningKey, vote) -> str:
    """signs a vote with the given key and returns the signature as hexstring"""
    return sign_message(private_key, vote.unsigned_hash())


def verify_vote_sig(vote, signature: str, address="") -> bool:
    """verifies a vote signature"""
    if address == "":
        return verify_message(address_to_key(vote.get_sender_address()), vote.unsigned_hash(), signature)
    else:
        return verify_message(address_to_key(address), vote.unsigned_hash(), signature)


def get_transaction_sig(private_key: ecdsa.SigningKey, transaction) -> str:
    """
    signs a transaction with the given key and returns signature as hexstring
    WARNING:
    This method is for internal use only. 
    Use Wallet().sign_transaction(). 
    Otherwiese the nonce of the tx will be wrong, hence the signature will be wrong
    """
    return sign_message(private_key, transaction.unsigned_hash())


def verify_transaction_sig(transaction, signature: str, address="") -> bool:
    """verifys that a given transaction is signed with senders private key"""
    if address == "":
        return verify_message(address_to_key(transaction.get_sender_address()), transaction.unsigned_hash(), signature)
    else:
        return verify_message(address_to_key(address), transaction.unsigned_hash(), signature)
