Assumptions that needed to be made that the paper dose not state.
- Types:
    - Everything is a HexString
        - excluding Addresses
    - or List[HexString]
    - Hashing works with "0x_" excluded
    - Blocks (and Shards) and Tx are dicts of HexString
    - Block and Tx Hashes are hashes of the JsonDict of the blocks

- Transaction:
    - a transaction is valid if the public_key generated from sender_address validates the unsigned_hash of the transaction against the transactions signature
    - nonce is counted from 0 to n
    - TODO: fee (is it in neutro? or in fractions/parts of neutro?)

- Transaction Nonces
    -the next nonce is strictly bound to last deployed transaction. So if my transaction is not in a block I cannot publish another one

- Voting Token Transactions
    -are only exchanges from Voting Tokens for Neutro
    -because of that they need to be signed by both parties
    -they are issued by the voting token sender
    
- Wallet:
    - nonce is counted from 0 to n
    - using ECDSA 

- Neutro Consensus:
    -validation token transactions are only main chain
    -voting client behaviour:
        -just for the prototype "first block I see, I vote for" 
    -there is a fixed amount of voting tokens 
        -TODO amount?

- Shard Blocks:
    -they also contain a "previous_hash" field, so that finding the main block of a shard is just going to previous_block_number + 1.
    -shard blocks are also chained
        -even over main blocks boundaries, this makes it easy to parse the shard chain for light client

- Address:
    - using base58 of ECDSA public_key as address

- pow:
    - difficulty is in HexString format, a Block is valid if hash(Block) <= difficulty
    - nonces used for mining are also hexString of length 8 byte (16 hex values)
        -this gives a range of 2^(64) possible blocks with the exact same configuration
    -difficulty adjustment needs to be synchronized, so there should be one point in time each day/week/lunar/month where all nodes reach consensus on the new difficulty

- database:
    - everything is stored in /repo_root/.data/
        - wallets are stored as /wallet/address, /wallet/private, /wallet/nonce
        - blocks are stored as /blocks/{block_height}.block
        - block_hash(es) are linked to block_height in /blocks/hash.dictionary

-client:
    -a block is deemed stable (confirmed) if there are 7 blocks after it and tere are no forks in that time

Possible Optimisations and also help wanted:
    -database
        -restructure all the db stuff so we acually have a database
            -rework to use something like mongodb (or maybe something that is "light" and not so powerfull as mongodb)
            -another idea: mariaDB
                -there is a python library for mariadb(https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/)
    -make client smarter
        -start mining wehn not all shards are there (because 2/3 +1 shards are a valid block)
    -rework consensus so that there is no downtime for tx throuput while mining main block
    -adding more votes to a single broadcast package