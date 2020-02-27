from helper import *

class Node:
	def __init__(self, node_id, m, successor=None, predecessor=None):
		self.m = m
		self.HT = {} # Hash Table // DS
		self.node_id = node_id

		self.predecessor = predecessor
		self.finger_table = [successor]

	def update_finger_table(self, chord):
		del self.finger_table[1:]
		for i in range(1, self.m):
			self.finger_table.append(chord.find_successor(self.node_id + (2**i)))


	def print(self):
		print("[@] ID: ", self.node_id)
		print("\t[.] predecessor ID: ", self.predecessor.node_id)
		print("\t[.] successor ID: ", self.finger_table[0].node_id)
		# print("[.] Finger table: ")
		# for i in range(self.m):
		# 	print("i: {} {}".format(i, self.finger_table[i]))
		print("\t[.] Data: ", self.HT)
		print("-"*50)