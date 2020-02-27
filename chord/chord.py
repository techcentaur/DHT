from node import Node


def dist(id1, id2):
	"""id1 and id2 are integers"""
	return id1-id2

class Chord:
	def __init__(self, m):
		# chord init and first node
		self.m = m
		self.num_nodes = 2 ** m

		self.first_node = Node(0)
		self.first_node.finger_table[0] = self.first_node

		self.first_node.predecessor = -1
		self.first_node.update_finger_table(self, self.m)


	def get_node(self, first_node, key):
		return first_node.find_successor(key)

	def lookup(self, key):	
		where = self.get_node(self.first_node, key)
		if key in where.HT:
			return where.HT[key]
		
		# print("[?] No saved value for key!")
		return -1

	def insert(self, key, value):
		where = self.get_node(self.first_node, key)
		where.HT[key] = value

		return 1

	def join(self, new_node):
		pass

	def leave(self, new_node):
		pass




