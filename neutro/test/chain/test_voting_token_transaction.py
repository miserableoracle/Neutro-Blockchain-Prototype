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
    vtx = VotingTokenTransaction(sender, receiver, vt_amount, nto_amount)

    assert vtx.string() == \
        '{"sender": "iWVjc8hWuRuePAv1X8nDZdcjKcqivDUH62YKhBXBHqp2yGfgeXyHJDj5XwCHwjWB6GevCjMYT59XSBiQvMYHQ4P", "receiver": "3wWwKC6CGqNo2gJqeSUc5gm91LKt2n8KKiiZYYjYHJBawDrsBPwaFwcMQX9HwDy56msMZqYVHauVkLQQfz3kiU8d", "vt_amount": 100, "nto_amount": 100, "sender_nonce": 0, "receiver_nonce": 0, "sender_signature": "", "receiver_signature": ""}'
    assert vtx.hash() == "6c2a4166cc83fab82ba8716928c68b0a16704dc84a83623d7ba4a26493b52f50"


def test_unsigned_hash():
    sender = "0"
    receiver = "1"
    vt_amount = 100
    nto_amount = 100
    vtx = VotingTokenTransaction(sender, receiver, vt_amount, nto_amount)
    vtx_signed_hash = vtx.hash()
    vtx_unsigned_hash = vtx.unsigned_hash()
    # no signature means equivalent hashes
    assert vtx_signed_hash == vtx_unsigned_hash
    vtx.sender_signature = "a"
    # assert signed hash has changed
    assert vtx.hash() != vtx_signed_hash
    # assert unsigned didnt
    assert vtx.unsigned_hash() == vtx_unsigned_hash
    vtx_signed_hash2 = vtx.hash()
    vtx.receiver_signature = "b"
    # assert signed hash has changed
    assert vtx.hash() != vtx_signed_hash2
    # assert unsigned didnt
    assert vtx.unsigned_hash() == vtx_unsigned_hash


def test_vtx_from_json():
    """test serialization and deserialization"""
    sender = "0"
    receiver = "1"
    vt_amount = 100
    nto_amount = 100
    t1 = VotingTokenTransaction(sender, receiver, vt_amount, nto_amount)
    t2 = voting_token_transaction.from_json(t1.string())
    assert t1.string() == t2.string()
    assert t1.hash() == t2.hash()
    assert t1.unsigned_hash() == t2.unsigned_hash()


def test_verify_vtx_signature():
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
    sender_wallet.sign_vtx_sender(t)
    # verify sender signature
    assert cryptoutil.verify_transaction_sig(
        t, t.get_sender_signature(), t.get_sender())
    # tx not valid because receiver did not sign
    assert False == t.verify()
    # sign with receiver
    receiver_wallet.sign_vtx_receiver(t)
    # should work
    assert cryptoutil.verify_transaction_sig(
        t, t.get_receiver_signature(), t.get_receiver())
    # should also work
    assert t.verify()
