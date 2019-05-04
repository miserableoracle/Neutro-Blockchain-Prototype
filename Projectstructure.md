### stuff, suggestion:
*this is a suggestion, this might change as we go*
- we use the code style convention from https://www.python.org/dev/peps/pep-0008/
- we are using pytest https://pythontesting.net/framework/pytest/pytest-introduction/ *doctest is not allowed*
- we follow this guide when commenting/documenting https://realpython.com/documenting-python-code/ *including type-hinting* but we don't do it the suggested way for ClassDocstrings and PackageDockstrings (too much work).

- we indent using 4 spaces ?!

### project structure suggestion:
*this is also a suggestion, might change as we go*
```
- src
    - client
        - validation *maybe this whole validation thing can be done within the classes themselfs?*
            - validate_main_block.py
            - validate_shard_block.py
            - validate_tx.py
            - validate_vote.py
            - validate_pow.py
        - p2p
        - *another milestone TODO*
        - full_client
            - full_client.py
            - full_client_config.json
        - light_client
            - light_client.py
            - light_client_config.json
    - chain
        - main_block.py
        - shard_block.py
        - transaction.py
        - trie
            - trie.py
            - trie_db.py
    - util
        - types.py 
            - *https://docs.python.org/3/library/typing.html*
        - hashutil.py 
            - *sha256?*
        - cryptoutil.py 
            - *ecdsa?*
        - addressutil.py
            - *bitcoins Base58*
        - loggerutil.py
            - *any framework? or just standard pythonlogging?* 
    - consensus
        - *another milestone TODO*
        - vote.py
        - pow.py
    - database
        - db.py
        - account.py
        - block_pool.py
        - tx_pool.py
        - vote_pool.py
    - config
        - config.py
        - string.json
            - *for string constants*
        - config.json 
            - *json or xml or whatever?* 
- test
    - test_main_block.py
    - test_shard_block.py
    - test_transaction.py
    - test_trie.py
    - test_db.py
    - test_validate_tx.py
    - test_validate_main_block.py
    - test_validate_shard_block.py
    - test_p2p_boradcast_tx.py
    - test_p2p_boradcast_main_block.py
    - test_p2p_boradcast_shard_block.py
- doc
- setup.py
- requirements.txt
- README.md
- LICENSE
```

Any ideas?
missing:
    - genesis generation
    - license checking
    - 
