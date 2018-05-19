from hashlib2 import sha
from listlib import pad_to_power_of_n

class Tree:
    def __init__(self, data):
        if len(data) == 0:
            self.data = []
            self.root = LeafNode(0)
        else:
            self.data = pad_to_power_of_n(data, n=2)  # so we have an even path to root
            self.create_root()

    def create_proof(self, element):
        i = self.data.find(element)
        if i == -1:
            return False
        
        level_idx = 1
        proof = []
        while True:
            new_i = i // 2
            # TODO: this


    def create_root(self):
        # this is dumb way, should do this efficiently by only computing what needs to be computed
        # storing O(2^n) instead of O(n)
        """
            goes from the bottom row to the top, hashing together and creating left and right nodes bottom up
        """
        if len(self.data) == 0:
            current_level = [0,0]

        current_level = list(map(LeafNode, self.data))
        levels = [current_level]
        while len(current_level) >= 2:
            next_level = []
            left = None
            for d in current_level:
                if left is None:  # up to storing the left node
                    left = d 
                else:
                    right = d
                    node = NonLeafNode(left, right)
                    next_level.append(node)
                    left = None  # reset left as we stored it
            levels.append(current_level)
            current_level = next_level
        self.levels = levels
        self.root = current_level[0]


class NonLeafNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.data = sha( self.left.data + self.right.data )

class LeafNode:
    def __init__(self, data):
        self.data = sha(data) 
        self.non_hashed_data = data
