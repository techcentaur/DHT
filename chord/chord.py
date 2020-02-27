from node import Node
from helper import *

class Chord:
	def __init__(self, m):
		self.m = m
		self.num_nodes = 2**m

		self.first_node = Node(0, m, predecessor=-1)
		self.first_node.finger_table[0] = self.first_node
		self.first_node.update_finger_table(self.first_node)

	def lookup(self, key, verbose=False):	
		print("Look up {}".format(key), end='')
		__node = self.find_successor(key, verbose)
		if key in __node.HT:
			return __node.HT[key]
		return -1

	def find_successor():
		"""wrapper"""
		return self.first_node.find_successor(key, self.m)

	def insert(self, key, value):
		__node = self.find_successor(key)
		__node.HT[key] = value
		return 1

	def join(self, new_node):
		successor = self.find_successor(new_node.id)

		if successor.node_id == new_node.id:
			print("[?] Node with ID: {} exists in chord!".format(new_node.node_id))

		for key in successor.HT:
			d1 = dist(new_node.node_id, key)

			if not (d1<0):
				new_node.HT[key] = successor.HT[key]
				del successor.HT[key]

		tmp1 = successor.predecessor
		new_node.finger_table[0] = successor
		new_node.predecessor = tmp1

		successor.predecessor = new_node
		tmp1.finger_table[0] = new_node


		new_node.update_finger_table(self.m ,self.first_node)


	def leave(self, bye_node):
		for key, value in bye_node.HT.items():
			bye_node.finger_table[0].HT[key] = value

		if bye_node.finger_table[0] == bye_node:
			self.first_node = None
		else:
			bye_node.predecessor.finger_table[0] = bye_node.finger_table[0]
			bye_node.finger_table[0].predecessor = bye_node.predecessor

			if self.first_node == bye_node:
				self.first_node = bye_node.finger_table[0]
	

	def fix_fingers(self):
		self.first_node.update_finger_table(self.m, self.first_node)

		__next = self.first_node.finger_table[0]
		while __next != self.first_node:
			__next.update_finger_table(self.m, self.first_node)
			__next = __next.finger_table[0]

	def print(self):
		self.first_node.print()

		__next = self.first_node.finger_table[0]
		while __next != self.first_node:
			__next.print()
			__next = __next.finger_table[0]





