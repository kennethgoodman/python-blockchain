import os, json

def get_block_path(block_num):
    return '{}/{}'.format('blocks',block_num)

def get_block_header_path(block_num):
    return '{}/block_header.json'.format(get_block_path(block_num))

def get_block_data_path(block_num):
    return '{}/block_data.json'.format(get_block_path(block_num))

def get_block(block_num):
    with open(get_block_header_path(block_num), 'r') as infile:
        header = json.load(infile)
    with open(get_block_data_path(block_num), 'r') as infile:
        data = json.load(infile)
    return {
        'header' : header,
        'data': data
    }

def get_current_block_num():
    files = sorted(os.listdir('blocks'))
    if len(files) == 0:
        return 0
    return int(files[-1]) + 1

def get_all_blocks():
    # Highly innefficient, should prune
    c_block_num = get_current_block_num()
    blocks = {}
    for block_num in range(c_block_num):
        blocks[block_num] = get_block(block_num)
    return blocks

def get_prev_hash(block_num):
    if block_num == 0:
        raise ValueError("at genesis block, no prev hash")
    with open(get_block_header_path(block_num - 1), 'r') as infile:
        data = json.load(infile)
    return data['hash']
