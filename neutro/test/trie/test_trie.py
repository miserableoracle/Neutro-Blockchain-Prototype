from neutro.src.trie.trie import Trie
from neutro.src.chain.transaction import Transaction


def test_trie():
    txs = []
    for i in range(10):
        sender = "a" + str(i)
        receivers = [str(i)]
        amounts = [str(i + 100)]
        nonce = i
        fee = 100 * i
        txs.append(Transaction(sender, receivers, amounts, nonce, fee))
    txs = [tx.hash() for tx in txs]

    trie = Trie(txs)

    assert trie.size() == 10
    trie_root = trie.root()
    assert trie_root == "819208b7314e74647711cb43a22e518fea7d67541bd691ef7914a368883b43c6"


def test_trie_empty():
    trie = Trie()

    assert trie.size() == 0
    assert trie.root() == "f1534392279bddbf9d43dde8701cb5be14b82f76ec6607bf8d6ad557f60f304e"


def test_trie_only_one_tx():
    trie = Trie(["00af"])

    assert trie.size() == 1
    assert trie.root() == "a16a3ddd11708de93ce0cfd391fa9ecf9f55e0524fa76740affd6c41af8ac588"
