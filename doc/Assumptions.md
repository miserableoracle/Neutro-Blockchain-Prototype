Assumptions that needed to be made that the paper dose not state.
- Types:
	- Everything is a HexString
		- including Addresses
	- or List[HexString]
	- Hashing works with "0x_" excluded
	- Blocks (and Shards) and Tx are dicts of HexString
	- Block and Tx Hashes are hashes of the JsonDict of the blocks

- Transaction:
	- nonce is counted from 0 to n
	- fee 

- pow:
	- difficulty is in HexString format, a Block is valid if hash(Block) <= difficulty