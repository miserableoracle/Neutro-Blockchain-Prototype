from src.trie.trie import Trie
from src.chain.transaction import Transaction


def test_trie():
    txs = []
    for i in range(10):
        sender = None
        receivers = [str(i)]
        amounts = [str(i + 100)]
        nonce = i
        fee = 100 * i
        txs.append(Transaction(sender, receivers, amounts, nonce, fee))
    txs = [tx.hash() for tx in txs]

    trie = Trie(txs)

    assert trie.size() == 10
    trie_root = trie.root()
    assert trie_root == "bbfb85a7e47a5de5b4df101872fbd4f613a32972da875469c97a1ed0d5d22ab2"


def test_trie_empty():
    trie = Trie()

    assert trie.size() == 0
    assert trie.root() == "f1534392279bddbf9d43dde8701cb5be14b82f76ec6607bf8d6ad557f60f304e"
