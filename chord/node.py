class Node:
	def __init__(self, node_id,  successor=None, predecessor=None):
		self.HT = {} # Hash Table // DS

		self.node_id = node_id

		self.predecessor = predecessor
		self.finger_table = []
		if successor:
			self.finger_table.append(successor)


	def update_finger_table(self, chord, m):
		self.finger_table = [].append(self.finger_table[0])	

		for i in range(1, m):
			self.finger_table.append(self.find_successor(chord.first_node, self.node_id + (2**i)))
			# is this right?

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