from helper import *

class Node:
	def __init__(self, node_id,  successor=None, predecessor=None):
		self.HT = {} # Hash Table // DS
		self.node_id = node_id

		self.predecessor = predecessor
		self.finger_table = [successor]


	def update_finger_table(self, m, first_node):
		for i in range(1, m):
			if i < len(self.finger_table):
				self.finger_table[i] = first_node.find_successor(self.node_id + (2**i))
			else:
				self.finger_table.append(first_node.find_successor(self.node_id + (2**i)))

	def find_successor(self, key):
		if (dist(key, self.node_id) > 0) and (dist(self.finger_table[0], key) >= 0):
			return self.finger_table[0]
		else:
			__n = self.closest_preceding_node(key)
			return __n.find_successor(key)

	def closest_preceding_node(self, key):
		for i in range(self.m-1, -1, -1):
			if (dist(self.finger_table[i].node_id, n) > 0) and (dist(key, self.finger_table[i].node_id) < 0):
				return self.finger_table[i]
		return self			