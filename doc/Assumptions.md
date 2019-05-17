Assumptions that needed to be made that the paper dose not state.
- Types:
	- Everything is a HexString
		- excluding Addresses
	- or List[HexString]
	- Hashing works with "0x_" excluded
	- Blocks (and Shards) and Tx are dicts of HexString
	- Block and Tx Hashes are hashes of the JsonDict of the blocks

- Transaction:
	- nonce is counted from 0 to n
	- TODO: fee, is it in neutro? or in fractions/parts of neutro?

- Wallet:
	- nonce is counted from 0 to n
	- using ECDSA 

- Address:
	- using base58 of ECDSA pubKey as address

- pow:
	- difficulty is in HexString format, a Block is valid if hash(Block) <= difficulty