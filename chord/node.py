from helper import *

class Node:
	def __init__(self, node_id, m, successor=None, predecessor=None):
		self.m = m
		self.HT = {} # Hash Table // DS
		self.node_id = node_id

		self.predecessor = predecessor
		self.finger_table = [successor]

	def __hex_int_plus__(self, h1, h2):
		return hex((int('0x'+h1, 16) + h2) % 2**self.m)[2:]

	def update_finger_table(self, chord):
		del self.finger_table[1:]

		for i in range(1, self.m):
			if chord.distance=="integer":
				self.finger_table.append(chord.find_successor(self.node_id + 2**i))
			else:
				s = self.__hex_int_plus__(self.node_id, 2**i)
				self.finger_table.append(chord.find_successor(s))

	def print(self):
		print("[#] ID: {} | (predecessor, successor) -> ({} - {})".format(self.node_id, self.predecessor.node_id, self.finger_table[0].node_id))
		print("[$] Data: {}".format(self.HT))

	def print_finger_table(self):
		for i in  range(len(self.finger_table)):
			print("{} -> {}".format(i, self.finger_table[i].node_id))