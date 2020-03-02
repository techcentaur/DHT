from node import Node
from helper import *

class Chord:
	def __init__(self, m, dist="integer"):
		self.m = m
		self.distance = dist
		self.create()

	def create(self):
		if self.distance=="integer":
			self.first_node = Node(0, self.m)
		else:
			self.first_node = Node("0"*int(self.m/4), self.m)
		self.first_node.predecessor, self.first_node.finger_table[0] = self.first_node, self.first_node
		self.first_node.update_finger_table(self)

	def dist(self, id1, id2):
		if self.distance == "integer":
			if id1==id2:
				return 0
			if id1 < id2:
				return id2-id1
			return (2**self.m) - id1 + id2
		else:
			if id1==id2:
				return 0
			sub = (int('0x'+id2, 16) - int('0x'+id1, 16))
			if (int('0x'+id2, 16) > int('0x'+id1, 16)):
				return hex(sub)
			return hex((2**self.m + sub) % (2**self.m))

	def lookup(self, key, verbose=False):	
		__node, h = self.find_successor(key, hops=True)
		if key in __node.HT:
			return h
		return -1

	def get_hash(self, key):
		if self.distance=="integer":
			return key % 2**self.m
		else:
			return hex(int('0x'+key, 16) % (2**self.m))[2:]

	def find_successor(self, key, hops=False):
		h = 0
		
		__key = self.get_hash(key)
		pointer = self.first_node

		while True:
			if pointer.node_id == __key:
				if hops:
					return pointer, h
				return pointer
			if self.dist(pointer.node_id, __key) <= self.dist(pointer.finger_table[0].node_id, __key):
				if hops:
					return pointer.finger_table[0], h
				return pointer.finger_table[0]

			__node = pointer.finger_table[-1]
			i = 0
			while i < len(pointer.finger_table)-1:
				if self.dist(pointer.finger_table[i].node_id, __key) < self.dist(pointer.finger_table[i+1].node_id, __key):
					__node = pointer.finger_table[i]
				i += 1

			pointer = __node
			h += 1

	def insert(self, key, value):
		__node = self.find_successor(key)
		__node.HT[key] = value
		return 1

	def join(self, new_node):
		successor = self.find_successor(new_node.node_id)

		if successor.node_id == new_node.node_id:
			print("[?] Node with ID: {} exists in chord!".format(new_node.node_id))
			return -1

		for key in successor.HT:
			d1 = self.dist(new_node.node_id, k)

			if not (d1<0):
				new_node.HT[key] = successor.HT[key]
				del successor.HT[key]

		tmp1 = successor.predecessor
		new_node.finger_table[0] = successor
		new_node.predecessor = tmp1

		successor.predecessor = new_node
		tmp1.finger_table[0] = new_node

		new_node.update_finger_table(self)
		return 1


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





