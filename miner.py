from hashlib2 import sha
import os
import time
from block import Block, BlockFactory
from blockfinder import get_block_header_path, get_current_block_num, get_all_blocks, get_block
from binarylib import int_to_bin
from difficulty_adjustment import DA
from Transaction import Transaction
from node import Node

def mine_it(current_block, others_found_first_func, log_it=False):
	""" TODO: make this cypthon to speed it up """
	nonce = current_block.nonce
	target = 2**256 / current_block.difficulty - 1
	while not others_found_first_func(current_block.block_num):
		current_block.set_nonce(nonce)
		current_block.update_timestamp() 
		current_hash = sha(current_block.block_header)  # has nonce inside sha
		if log_it:
			print(nonce, current_hash, target)
		if current_hash < target:  # PoW here
			return current_block
		nonce += 1
	return None  # somebody else found the block first

def mine_it_pos(current_block, others_found_first_func, my_holdings, log_it=False):
	"""
		Can optimize so that we find as many blocks in the future as possible.
		Also try to fork blockchain? Nothing at stake problem 
		Add slashing
	"""
	target = (2**256 / current_block.difficulty - 1) * my_holdings
	while not others_found_first_func(current_block.block_num):
		current_block.update_timestamp() 
		current_hash = sha(current_block.block_data)  # no nonce here
		if current_hash < target:  # PoW here
			return current_block
		if log_it:
			print(current_hash)
		time.sleep(.1)  # can only find one block per timestamp
	return None  # somebody else found the block first

def standard_others_found_first_func(block_num):
	"""
	    look at blockchain at block_num and see if it exists
	"""
	return os.path.isfile(get_block_header_path(block_num))

def adjust_da(all_blocks, difficulties, rolling, n_back, target):
	new_difficulty_multiplier = DA(all_blocks, rolling=rolling, n_back=n_back, target=target)
	if rolling:
		ndm = max(min(new_difficulty_multiplier, 1.25), 0.75)
	else:
	    ndm = max(min(new_difficulty_multiplier, 4.00), 0.25)

	if rolling:
		if len(difficulties) > n_back:
			difficulty = ndm * difficulties[-n_back]
		else:
			difficulty = difficulties[0]
	else:
		difficulty = ndm * last_d
	return difficulty, ndm, new_difficulty_multiplier

def set_up_mining():
	""" TODO: use .env instead of hard-code """
	all_blocks = get_all_blocks() 
	if len(all_blocks) == 0:
	    block_num = 0  # genesis
	else:
	    block_num = max(all_blocks.keys()) + 1
	start_d = 5000.
	difficulties = [start_d]
	difficulty = start_d
	ndms = []
	rolling = True
	n_back  = 25
	target = .5
	bf = BlockFactory(block_num, start_d)
	return block_num, difficulties, ndms, rolling, n_back, target, all_blocks, bf

def main():
	block_num, difficulties, ndms, rolling, n_back, target, all_blocks, bf = set_up_mining()
	node = Node()
	while True:
		ndm, difficulty, block_data = mine_one(node, bf, block_num, all_blocks, difficulties, rolling, n_back, target)
		ndms.append(ndm)
		difficulties.append(difficulty)
		all_blocks[block_num] = block_data
		block_num += 1

def mine_one(node, bf, block_num, all_blocks, difficulties, rolling, n_back, target, send_block=True, log_it=False):
	difficulty, ndm, new_difficulty_multiplier = adjust_da(all_blocks, difficulties, rolling, n_back, target)
	print("difficulty = ", difficulty, ". new_difficulty_multiplier = ", new_difficulty_multiplier, ". ndm =", ndm)
	bf.difficulty = difficulty
	bf.block_num = block_num
	start = time.time()
	block = mine_it(bf.create_block(), lambda x: False, log_it=log_it)
	if block is not None: # someone else found a block first
		block.write_to_file()
    
    # if already found, do we need to read it?
	block_data = get_block(block_num)  # in the right format, TODO: decide if all blocks should be in Block format instead of json
	if block is not None and send_block:  # if we found it, need to send to all others
		node.send_block_to_all_peers(bf.block_num, block_data=block_data)

	print("found block {} with nonce {} and diff={}, took {} seconds".format(block.block_num, block.nonce, difficulty, time.time() - start))
	return ndm, difficulty, block_data

def test_time_to_mine():
	for difficulty in [1250000]: # range(100000,600000,50000):
		start = time.time()
		for _ in range(30):
			mine_it(Block(1, [Transaction.create_coinbase_tx()], 0, difficulty, test=True), lambda x: False, log_it=True)
		end = time.time()
		print("For difficulty={}, takes on average {} seconds".format(difficulty, (end-start)/25))

if __name__ == '__main__':
	test_time_to_mine()
    # main()

