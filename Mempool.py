

class Mempool:
	def __init__(self):
		self.txs = []  # TODO: should be a shorted list by transaction fee per byte

	def pop_transaction(self):
		return self.txs.pop()

	def get_all_transactions(self):
		rtn = self.txs
		self.txs = []
		return rtn

	def push_transaction(self, tx):
		self.txs.append(tx)

