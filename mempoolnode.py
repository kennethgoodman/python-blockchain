from flask import Flask, jsonify, request
from Transaction import Transaction
from Mempool import Mempool
from envlib import get_env
import json

app = Flask(__name__)
mempool = Mempool()

@app.route("/receive_tx", methods=['POST'])
def receive_tx():
	print(request.form)
	tx_data = request.json
	tx = Transaction.from_json(tx_data)
	if tx.verify():
		mempool.push_transaction(tx)
		return jsonify('received')
	else:
		raise NotImplementedError("Not sure what to do if tx is not valid")

@app.route("/get_txs", methods=['GET'])
def get_txs():
	txs_as_json = map(lambda tx: tx.default(), mempool.get_all_transactions())
	return jsonify(list(txs_as_json))

if __name__ == '__main__':
	app.run(debug=True, port=get_env('mempoolport',5000))