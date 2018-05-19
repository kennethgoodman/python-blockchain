import os, json, time, pathlib
from merkletree import Tree as MT
from hashlib2 import sha
from blockfinder import get_block_path, get_block_header_path, get_block_data_path, get_prev_hash, get_block
from Transaction import Transaction
from serializelib import serialize
from envlib import get_env
import requests

class BlockFactory:
    def __init__(self, block_num, difficulty):
        self.block_num = block_num
        self.difficulty = difficulty

    def create_block(self):
        return Block(
            block_num=self.block_num,
            transactions=[Transaction.create_coinbase_tx()],
            nonce=0,
            difficulty=self.difficulty,
            is_genesis=self.block_num == 0,
        )

    @staticmethod
    def get_transactions():
        json_txs = requests.get('127.0.0.1:' + str(get_env('mempoolport')) + "/get_txs").json

    @staticmethod
    def from_json(header, data):
        transactions = list(map(Transaction.from_json, data['transactions']))
        return Block(
            block_num=header['block_num'],
            transactions=transactions,
            nonce=header['nonce'],
            difficulty=header['difficulty'],
            is_genesis=header['block_num']==0,
            timestamp=header['timestamp'],
            block_hash=header['hash'],
            prev_hash=header['prev_hash'],
            merkle_root=header['transaction_merkle_root'],
        )

class Block:
    def __init__(self, block_num, transactions, nonce, difficulty, merkle_root=None, block_hash=None, prev_hash=None, is_genesis=False, test=False, timestamp=None):
        self.block_num = block_num
        self.transactions = transactions
        self.difficulty = difficulty
        self.nonce = nonce
        mt = MT(transactions)
        self.block_data = {'transactions': transactions}
        self.block_header = {'block_num':block_num,
         'nonce':nonce,
         'difficulty':difficulty,
         'transaction_merkle_root':mt.root.data if merkle_root is None else merkle_root,
         'timestamp':time.time() if timestamp is None else timestamp
        }
        if is_genesis:
            self.block_header['prev_hash'] = None
        elif prev_hash is not None:
            self.block_header['prev_hash'] = prev_hash
        else:
            if not test:
                self.block_header['prev_hash'] = get_prev_hash(self.block_num)
            else:
                self.block_header['prev_hash'] = None
        self.block_header['hash'] = sha(self.block_header) if block_hash is None else block_hash

    def verify_block(self):
        """
            1. Check prev block hash = current block prev hash
            2. Check MR(MT((transactions))) == MR
            3. Check all transactions are valid
        """
        def verify_prev_block_hash():
            if self.block_num == 0:
                return True
            return get_prev_hash(self.block_num) == self.block_header['prev_hash']
        
        def check_merkle_root():
            mt = MT(self.transactions)
            return mt.root.data = self.block_header['transaction_merkle_root']
        
        def check_all_transactions():
            return all(tx.verify() for tx in self.transactions)

        def verify_longest_chain():
            print("Have not checked: verify_longest_chain ")
            return True

        return verify_prev_block_hash() and check_merkle_root() and check_all_transactions() and verify_longest_chain()


    def set_nonce(self, nonce):
        self.nonce = nonce
        self.block_header['nonce'] = nonce

    def update_timestamp(self):
        self.block_header['timestamp'] = time.time()

    def write_to_file(self):
        path = get_block_path(self.block_num)
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        with open(get_block_data_path(self.block_num), 'w') as (outfile):
            json.dump(self.block_data, outfile, default=serialize)
        with open(get_block_header_path(self.block_num), 'w') as (outfile):
            json.dump(self.block_header, outfile, default=serialize)


def test():
    b = Block(0, [], 0, 0, is_genesis=True)
    b.write_to_file()
    b = Block(1, [1, 2], 0, 0)
    b.write_to_file()


if __name__ == '__main__':
    test()
