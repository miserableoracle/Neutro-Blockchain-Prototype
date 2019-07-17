import pytest
from neutro.src.chain import vote
from neutro.src.chain.vote import Vote
from neutro.src.util import wallet
from neutro.src.util import cryptoutil


def test_vote():
    prev_hash = "bc10b849a535b5be9f65fffb2e9c8809da75ff86590dd02e3ba26daf0c18b738"
    sender = "iWVjc8hWuRuePAv1X8nDZdcjKcqivDUH62YKhBXBHqp2yGfgeXyHJDj5XwCHwjWB6GevCjMYT59XSBiQvMYHQ4P"
    v = Vote(prev_hash, sender)

    assert v.string() == \
        '{"prev_hash": "bc10b849a535b5be9f65fffb2e9c8809da75ff86590dd02e3ba26daf0c18b738", "sender": "iWVjc8hWuRuePAv1X8nDZdcjKcqivDUH62YKhBXBHqp2yGfgeXyHJDj5XwCHwjWB6GevCjMYT59XSBiQvMYHQ4P", "signature": ""}'
    assert v.hash() == "0173a0d50cc20b880bf6822d866fc731333928acd45ebc1bfb62745b4bb10a5d"


def test_vote_from_json():
    v = Vote("prev_hash", "sender", "signature")
    v_copy = vote.from_json(v.string())
    assert v.prev_hash == v_copy.prev_hash
    assert v.sender == v_copy.sender
    assert v.signature == v_copy.signature


def test_sign_vote_valid():
    w = wallet.generate_new_wallet()
    prev_hash = "0"
    sender = w.get_address()
    v = Vote(prev_hash, sender)
    w.sign_vote(v)
    assert cryptoutil.verify_vote_sig(v, v.signature, v.sender)
    with pytest.raises(AssertionError):
        cryptoutil.verify_vote_sig(v, "")


def test_sign_vote_invalid_address():
    prev_hash = "bc10b849a535b5be9f65fffb2e9c8809da75ff86590dd02e3ba26daf0c18b738"
    sender = "iWVjc8hWuRuePAv1X8nDZdcjKcqivDUH62YKhBXBHqp2yGfgeXyHJDj5XwCHwjWB6GevCjMYT59XSBiQvMYHQ4P"
    v = Vote(prev_hash, sender)

    w = wallet.generate_new_wallet()
    with pytest.raises(ValueError):
        w.sign_vote(v)
