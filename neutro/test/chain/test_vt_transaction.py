import pytest
from neutro.src.chain import voting_token_transaction
from neutro.src.chain.voting_token_transaction import VotingTokenTransaction
from neutro.src.util import cryptoutil
from neutro.src.util import wallet


def test_voting_token_transaction():
    sender = "iWVjc8hWuRuePAv1X8nDZdcjKcqivDUH62YKhBXBHqp2yGfgeXyHJDj5XwCHwjWB6GevCjMYT59XSBiQvMYHQ4P"
    receiver = "3wWwKC6CGqNo2gJqeSUc5gm91LKt2n8KKiiZYYjYHJBawDrsBPwaFwcMQX9HwDy56msMZqYVHauVkLQQfz3kiU8d"
    vt_amount = 100
    nto_amount = 100
    vt_tx = VotingTokenTransaction(sender, receiver, vt_amount, nto_amount)

    assert vt_tx.string() == \
        '{"sender_address": "iWVjc8hWuRuePAv1X8nDZdcjKcqivDUH62YKhBXBHqp2yGfgeXyHJDj5XwCHwjWB6GevCjMYT59XSBiQvMYHQ4P", "receiver_address": "3wWwKC6CGqNo2gJqeSUc5gm91LKt2n8KKiiZYYjYHJBawDrsBPwaFwcMQX9HwDy56msMZqYVHauVkLQQfz3kiU8d", "vt_amount": 100, "nto_amount": 100, "sender_nonce": 0, "receiver_nonce": 0, "sender_signature": "", "receiver_signature": ""}'
    assert vt_tx.hash() == "7433a8bdfd8dd2687c72781e1ea7cb2d4c8d48b0c4197df8ded4c023a6d70b8f"


def test_unsigned_hash():
    sender = "0"
    receiver = "1"
    vt_amount = 100
    nto_amount = 100
    vt_tx = VotingTokenTransaction(sender, receiver, vt_amount, nto_amount)
    vt_tx_signed_hash = vt_tx.hash()
    vt_tx_unsigned_hash = vt_tx.unsigned_hash()
    # no signature means equivalent hashes
    assert vt_tx_signed_hash == vt_tx_unsigned_hash
    vt_tx.sender_signature = "a"
    # assert signed hash has changed
    assert vt_tx.hash() != vt_tx_signed_hash
    # assert unsigned didnt
    assert vt_tx.unsigned_hash() == vt_tx_unsigned_hash
    vt_tx_signed_hash2 = vt_tx.hash()
    vt_tx.receiver_signature = "b"
    # assert signed hash has changed
    assert vt_tx.hash() != vt_tx_signed_hash2
    # assert unsigned didnt
    assert vt_tx.unsigned_hash() == vt_tx_unsigned_hash


def test_vt_tx_from_json():
    """test serialization and deserialization"""
    sender = "0"
    receiver = "1"
    vt_amount = 100
    nto_amount = 100
    t1 = VotingTokenTransaction(sender, receiver, vt_amount, nto_amount)
    t2 = voting_token_transaction.from_json_string(t1.string())
    assert t1.string() == t2.string()
    assert t1.hash() == t2.hash()
    assert t1.unsigned_hash() == t2.unsigned_hash()


def test_verify_vt_tx_signature():
    """
    tests if sender and receiver sigs can be validated seperately and together
    """
    sender_wallet = wallet.generate_new_wallet()
    receiver_wallet = wallet.generate_new_wallet()
    sender = sender_wallet.get_address()
    receiver = receiver_wallet.get_address()
    vt_amount = 100
    nto_amount = 100
    t = VotingTokenTransaction(sender, receiver, vt_amount, nto_amount)
    sender_wallet.sign_voting_token_transaction_sender(t)
    # verify sender signature
    assert cryptoutil.verify_transaction_sig(
        t, t.get_sender_signature(), t.get_sender_address())
    # tx not valid because receiver did not sign
    assert False == t.verify()
    # sign with receiver
    receiver_wallet.sign_voting_token_transaction_receiver(t)
    # should work
    assert cryptoutil.verify_transaction_sig(
        t, t.get_receiver_signature(), t.get_receiver_address())
    # should also work
    assert t.verify()
