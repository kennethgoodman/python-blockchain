from miner import mine_one, set_up_mining
from node import Node
from node import send_block_to_all_peers

def main():
	node = Node()
	block_num, difficulties, ndms, rolling, n_back, target, all_blocks, bf = set_up_mining()
	_, _, block_data = mine_one(node, bf, block_num, all_blocks, difficulties, rolling, n_back, target, send_block=False, log_it=False)
	send_block_to_all_peers(block_num, block_data=block_data, test=False)

if __name__ == '__main__':
	main()
