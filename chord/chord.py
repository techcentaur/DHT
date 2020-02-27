from node import Node


class Chord:
	def __init__(self, m):
		# chord init and first node
		self.m = m
		self.num_nodes = 2 ** m

		self.first_node = Node(0)
		self.first_node.finger_table[0] = self.first_node

		self.first_node.predecessor = -1
		self.first_node.update_finger_table(self, self.m)


