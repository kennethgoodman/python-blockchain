


There are a couple parts to this:

mine: `$ python3 miner.py`
listen and relay other blocks: `$ python3 node.py` - will also sort mempool, can run in SPV mode also: `$ python3 node.py --spv`
mempool: `$python3 mempoolnode.py >logs/mempool/log.out 2> logs/mempool/log.err &` 
create transactions: `$ python3 wallet.py`

Design Choices:

I decided to use different local nodes for mempool, mining, wallet, UTXO and node so that each could be compartmentalized. The rage these days is microservices and I agree that it is easier to understand code when it is seperated by usecase, even if code is duplicated and slow.

Feel free to fork, use as you wish and pull request.

All criticism is welcome.

I know that not everything in this repo is exactly how Bitcoin or other blockchains work, or that it is entirely secure (I don't even verify scripts yet....), but I think many will be able to learn how blockchains work by reading relatively few lines of code in Python. 