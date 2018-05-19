"""
TODO: 
	1. Networking 
		first on localhost
		Then as an open server
			DDoS attack
"""
from flask import Flask, jsonify, request
from envlib import get_env
import json
from blockfinder import get_block, get_current_block_num
import requests
from block import BlockFactory
from Transaction import Transaction



class Node:
	def __init__(self):
		""" TODO: switch over to flask-restful """

	@property
	def peers(self):
		for peer_url in get_env('peers').split(','):
			yield peer_url

	def prosses_received_block(self, block_data):
		header, body = block_data['header'], block_data['data']
		block = BlockFactory.from_json(header, body)
		if block.verify():
			block.write_to_file()
		else:
			raise NotImplementError("Not sure what to do when not valid block. Header = {}, body = {}".format(header, body))

	def get_latest_blocknum_from_peers(self):
		""" TODO: What happens if one peer is off chain """
		max_block = get_current_block_num()
		max_peer = None
		for peer in self.peers:
			latest_block = int(requests.get(peer + 'latest_block').text)
			if latest_block > max_block:
				max_block = latest_block
				max_peer = peer
		return {'max_block': max_block, 'peer': max_peer}

	def get_block_from_peer(self, peer, blocknum):
		url = peer + "get_block/" + str(blocknum)
		return requests.get(url).json()

	def catch_up_from_peers(self):
		up_to = get_current_block_num()
		latest = self.get_latest_blocknum_from_peers()
		print(latest)
		if latest['peer'] is None:
			return
		for blocknum in range(up_to, latest['max_block'] + 1):  
			blockdata = self.get_block_from_peer(latest['peer'], blocknum)
			self.prosses_received_block(blockdata)

	def send_block(blocknum, peer_url, data=None):
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		if data is None:
			data = json.dumps({'block_data': get_block(blocknum)})
		return requests.post(peer_url + "receive_block/{}".format(blocknum), data=data, headers=headers)

	def send_block_to_all_peers(self, blocknum, block_data=None, test=False):
		print("in send_block_to_all_peers")
		if block_data is None:
			data = json.dumps(get_block(blocknum))
		else:
			data = block_data

		for peer_url in get_env('peers').split(','):
			if test:
				print(requests.post(peer_url).json())
			else:
				print(self.send_block(blocknum, peer_url).json())
			print("sent block")

app = Flask(__name__)

@app.route("/receive_tx", methods=['POST'])
def receive_tx():
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	return requests.post('127.0.0.1:' + get_env('mempoolport') + "/receive_tx", data=request.json, headers=headers)

@app.route("/get_block/<blocknum>", methods=['GET'])
def get_block_by_num(blocknum):
	return jsonify(get_block(blocknum))

@app.route("/receive_block/<blocknum>", methods=['POST'])
def receive_block(blocknum):
	print("at receive_block")
	block_data = request.json.get('block_data')
	node.prosses_received_block(blockdata)
	# send_block_to_all_peers(blocknum, block_data=block) TODO: don't uncomment until code there to stop sending in an endless recursive manner
	return jsonify('received')

@app.route("/latest_block", methods=['GET'])
def latest_block():
	return jsonify(get_current_block_num() - 1)

@app.route("/send_block/<blocknum>", methods=['POST'])
def send_block(blocknum):
	print("at send_block")
	print(request.form)
	block = request.json.get('block_data',None)
	node.send_block_to_all_peers(blocknum, block_data=block)
	# send_block_to_all_peers(blocknum, block_data=block) TODO: don't uncomment until code there to stop sending in an endless recursive manner
	return jsonify('received')

if __name__ == '__main__':
	node = Node()
	node.catch_up_from_peers()
	app.run(debug=True, port=get_env('port'))