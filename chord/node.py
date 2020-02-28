from helper import *

class Node:
	def __init__(self, node_id, m, successor=None, predecessor=None):
		self.m = m
		self.HT = {} # Hash Table // DS
		self.node_id = node_id

		self.predecessor = predecessor
		self.finger_table = [successor]

	def update_finger_table(self, chord):
		tmp_table = [self.finger_table[0]]
		for i in range(1, self.m):
			tmp_table.append(chord.find_successor(self.node_id + (2**i)))
		self.finger_table = tmp_table

	def print(self):
		print("[#] ID: {} | (predecessor, successor) -> ({} - {})".format(self.node_id, self.predecessor.node_id, self.finger_table[0].node_id))
		# print("\t[.] Data: ", self.HT)
