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
    assert trie_root == "ad091a174423f37617c3abe27bb53dd13d8da5706308c16e2a40f59e9cdb11ee"


def test_trie_empty():
    trie = Trie()

    assert trie.size() == 0
    assert trie.root() == "f1534392279bddbf9d43dde8701cb5be14b82f76ec6607bf8d6ad557f60f304e"


def test_trie_only_one_tx():
    trie = Trie(["00af"])

    assert trie.size() == 1
    assert trie.root() == "a16a3ddd11708de93ce0cfd391fa9ecf9f55e0524fa76740affd6c41af8ac588"
