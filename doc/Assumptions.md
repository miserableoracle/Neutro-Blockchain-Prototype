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

- Wallet:
	- nonce is counted from 0 to n
	- using ECDSA 

- Address:
	- using base58 of ECDSA public_key as address

- pow:
	- difficulty is in HexString format, a Block is valid if hash(Block) <= difficulty


- database:
	- everything is stored in /repo_root/.data/
		- wallets are stored as /wallet/address, /wallet/private, /wallet/nonce
		- blocks are stored as /blocks/{block_height}.block
		- block_hash(es) are linked to block_height in /blocks/hash.dictionary