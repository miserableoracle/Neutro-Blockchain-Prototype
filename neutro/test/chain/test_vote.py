import pytest
from neutro.src.chain import vote
from neutro.src.chain.vote import Vote
from neutro.src.util import wallet
from neutro.src.util import cryptoutil


def test_vote():
    prev_hash = "bc10b849a535b5be9f65fffb2e9c8809da75ff86590dd02e3ba26daf0c18b738"
    sender = "iWVjc8hWuRuePAv1X8nDZdcjKcqivDUH62YKhBXBHqp2yGfgeXyHJDj5XwCHwjWB6GevCjMYT59XSBiQvMYHQ4P"
    nonce = "0x00fabcde"
    v = Vote(prev_hash, sender, nonce)

    assert v.string() == \
        '{"prev_hash": "bc10b849a535b5be9f65fffb2e9c8809da75ff86590dd02e3ba26daf0c18b738", "sender": "iWVjc8hWuRuePAv1X8nDZdcjKcqivDUH62YKhBXBHqp2yGfgeXyHJDj5XwCHwjWB6GevCjMYT59XSBiQvMYHQ4P", "nonce": "0x00fabcde", "signature": ""}'
    assert v.hash() == "c51224bc79c4b5b71b72007f5ddef375fbc4d35fa9dbbf3133635fc6363090d4"


def test_vote_from_json_string():
    v = Vote("prev_hash", "sender", "nonce", "signature")
    v_copy = vote.from_json_string(v.string())
    assert v.prev_hash == v_copy.prev_hash
    assert v.sender == v_copy.sender
    assert v.nonce == v_copy.nonce
    assert v.signature == v_copy.signature


def test_sign_vote_valid():
    w = wallet.generate_new_wallet()
    prev_hash = "0"
    sender = w.get_address()
    nonce = "0"
    v = Vote(prev_hash, sender, nonce)
    w.sign_vote(v)
    assert cryptoutil.verify_vote_sig(v, v.signature, v.sender)


def test_sign_vote_invalid_address():
    prev_hash = "bc10b849a535b5be9f65fffb2e9c8809da75ff86590dd02e3ba26daf0c18b738"
    sender = "iWVjc8hWuRuePAv1X8nDZdcjKcqivDUH62YKhBXBHqp2yGfgeXyHJDj5XwCHwjWB6GevCjMYT59XSBiQvMYHQ4P"
    nonce = "0x00fabcde"
    v = Vote(prev_hash, sender, nonce)

    w = wallet.generate_new_wallet()
    with pytest.raises(ValueError):
        w.sign_vote(v)
