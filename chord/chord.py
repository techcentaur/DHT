from node import Node
from helper import *

class Chord:
	def __init__(self, m):
		self.m = m
		self.num_nodes = 2**m

		self.first_node = Node(0, m)
		self.first_node.predecessor = self.first_node
		self.first_node.finger_table[0] = self.first_node
		
		self.first_node.update_finger_table(self)

	def dist(self, id1, id2):
		if id1==id2:
			return 0
		if id1 < id2:
			return id2-id1
		return self.num_nodes - id1 + id2


	def lookup(self, key, verbose=False):	
		print("Look up {}".format(key), end='')
		__node = self.find_successor(key, verbose)
		if key in __node.HT:
			return __node.HT[key]
		return -1

	def get_hash(self, key):
		return key % self.num_nodes

	def find_successor(self, key, verbose=False):
		__key = self.get_hash(key)
		pointer = self.first_node

		# if verbose:
		# 	print(": {}".format(pointer.node_id), end='')
		first=True
		while True:
			if verbose:
				if first:
					first=False
					print(": {}".format(pointer.node_id), end='')
				else:
					print("-> {}".format(pointer.node_id), end='')
			if pointer.node_id is __key:
				if verbose:
					print("-> {}".format(pointer.node_id), end='')
				return pointer

			if self.dist(pointer.node_id, __key) <= self.dist(pointer.finger_table[0].node_id, __key):
				if verbose:
					print("-> {}".format(pointer.finger_table[0].node_id), end='')
				return pointer.finger_table[0]
			
			__node = pointer.finger_table[-1]

			i = 0
			bound = len(pointer.finger_table)-1
			while i < bound:
				if self.dist(pointer.finger_table[i].node_id, __key) < self.dist(pointer.finger_table[i+1].node_id, __key):
					__node = pointer.finger_table[i]
				i += 1

			pointer = __node

	def insert(self, key, value):
		__node = self.find_successor(key)
		__node.HT[key] = value
		return 1

	def join(self, new_node):
		successor = self.find_successor(new_node.node_id)

		if successor.node_id == new_node.node_id:
			print("[?] Node with ID: {} exists in chord!".format(new_node.node_id))
			return

		for key in successor.HT:
			d1 = self.dist(new_node.node_id, k)

			if not (d1<0):
				new_node.HT[key] = successor.HT[key]
				del successor.HT[key]

		# stabilization		
		tmp1 = successor.predecessor
		new_node.finger_table[0] = successor
		new_node.predecessor = tmp1

		# notify
		successor.predecessor = new_node
		tmp1.finger_table[0] = new_node

		new_node.update_finger_table(self)


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
	
	def leave_node_by_key(self, key):
		res = self.find_node_by_key(key)
		if res == -1:
			return 
		else:
			self.leave(res)
			print("[*] removed successfully")


	def find_node_by_key(self, key):
		if key==self.first_node.node_id:
			return self.first_node

		__next = self.first_node.finger_table[0]
		while __next != self.first_node:
			if key==__next.node_id:
				return __next
			__next = __next.finger_table[0]

		print("[?] Node ID {} doesn't exist!".format(key))
		return -1

	def fix_fingers(self):
		self.first_node.update_finger_table(self)

		__next = self.first_node.finger_table[0]
		while __next != self.first_node:
			__next.update_finger_table(self)
			__next = __next.finger_table[0]

	def print(self):
		self.first_node.print()

		__next = self.first_node.finger_table[0]
		while __next != self.first_node:
			__next.print()
			__next = __next.finger_table[0]





