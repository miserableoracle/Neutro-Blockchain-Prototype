from neutro.src.chain.vote import Vote


def test_vote():
    prev_hash = "bc10b849a535b5be9f65fffb2e9c8809da75ff86590dd02e3ba26daf0c18b738"
    sender = "iWVjc8hWuRuePAv1X8nDZdcjKcqivDUH62YKhBXBHqp2yGfgeXyHJDj5XwCHwjWB6GevCjMYT59XSBiQvMYHQ4P"
    nonce = "0x00fabcde"
    v = Vote(prev_hash, sender, nonce)

    assert v.string() == \
        '{"prev_hash": "bc10b849a535b5be9f65fffb2e9c8809da75ff86590dd02e3ba26daf0c18b738", "sender": "iWVjc8hWuRuePAv1X8nDZdcjKcqivDUH62YKhBXBHqp2yGfgeXyHJDj5XwCHwjWB6GevCjMYT59XSBiQvMYHQ4P", "nonce": "0x00fabcde", "signature": ""}'
    assert v.hash() == "c51224bc79c4b5b71b72007f5ddef375fbc4d35fa9dbbf3133635fc6363090d4"
