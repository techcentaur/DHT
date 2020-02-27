from helper import *

class Node:
	def __init__(self, node_id, m, successor=None, predecessor=None):
		self.m = m
		self.HT = {} # Hash Table // DS
		self.node_id = node_id

		self.predecessor = predecessor
		self.finger_table = [successor]

	def update_finger_table(self, first_node):
		for i in range(1, self.m):
			if i < len(self.finger_table):
				self.finger_table[i] = first_node.find_successor(self.node_id + (2**i))
			else:
				self.finger_table.append(first_node.find_successor(self.node_id + (2**i)))

	def dist(self, id1, id2):
		if id1==id2:
			return 0
		return (id1-id2) % (2**self.m)

	def find_successor(self, key, verbose=False):
		if self.node_id == key:
			return self.node_id
		if (self.dist(key, self.node_id) > 0) and (self.dist(self.finger_table[0].node_id, key) >= 0):
			if verbose:
				print(": {}".format(self.finger_table[0].node_id), end='')
			
			return self.finger_table[0]
		else:
			__n = self.closest_preceding_node(key)
			if verbose:
				print("-> {}".format(self.finger_table[0].node_id), end='')

			return __n.find_successor(key, verbose)

	def closest_preceding_node(self, key):
		for i in range(len(self.finger_table)-1, -1, -1):
			if (self.dist(self.finger_table[i].node_id, self.node_id) > 0) and (self.dist(key, self.finger_table[i].node_id) < 0):
				return self.finger_table[i]
		return self			


	def print(self):
		print("="*30)
		print("[.] ID: ", self.node_id)
		print("[.] predecessor ID: ", self.predecessor.node_id)
		print("[.] successor ID: ", self.finger_table[0].node_id)
		# print("[.] Finger table: ")
		# for i in range(self.m):
		# 	print("i: {} {}".format(i, self.finger_table[i]))
		print("[.] Data: ", self.HT)
		print("="*30)