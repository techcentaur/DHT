class Node:
	def __init__(self, node_id,  succ=None, pred=None):
		self.HT = {} # Hash Table // DS

		self.node_id = node_id
		self.pred = pred
		
		self.finger_table = []
		if succ:
			self.finger_table.append(succ)


	def update_finger_table(self):
		pass