import math
import hashlib
from helper import hex_distance

b = 2
N = 100


class Node():
	def __init__(self, hash_string):
		self.hash_string = hash_string
		self.R = []

		for i in range(math.ceil(math.log(N, pow(2, b)))):
			self.R.append([])
			for j in range(pow(2, b)):
				self.R[i].append(None)

		self.M = [None for x in range(pow(2, b+1))]
		# [min, max]
		self.L = [[None for x in range(pow(2, b-1))], [None for x in range(pow(2, b-1))]] 


	def print_tables(self):
		print("[*] Node id: ", self.hash_string)
		print("[#] Routing Table:")
		for x in self.R:
			print(x)
		print("[#] Neighborhood Set: \n", self.M)
		print("[#] Leaf Set: \n", self.L)

	def forward_if_in_leaf_set_range(self, D):
		minL = None
		minPresent = False
		for i in self.L[0]:
			if i is not None:
				if D >= i:
					ret = id_compare(D, i)
					if minL is None:
						minL = ret
						minPresent = True
					elif minL[0] < ret[0]:
						minL = ret
					elif minL[0] == ret [0] and minL[1] > ret[1]:
						minL = ret

		maxL = None
		maxPresent = False
		for i in self.L[1]:
			if i is not None:
				if D <= i:
					ret = id_compare(D, i)
					if maxL is None:
						maxL = ret
						maxPresent = True
					elif maxL[0] < ret[0]:
						maxL = ret
					elif maxL[0] == ret [0] and maxL[1] > ret[1]:
						maxL = ret

		if (not minPresent) and (not maxPresent):
			return (True, )

	def forward(self, msg, key):
		if msg.lower()=="join":
			# all of the middle nodes have to send their tables
		else:
			pass

	def routing(self, msg, key):
		if len(key) is not 128:
			D = hashlib.md5(key.encode()).hexdigest() 

		# see in leaf set
		# self.forward_if_in_leaf_set_range(D)
		t = False
		if t:
			# forward to node found in leaf set
			pass
		else:
			I = self.common_prefix(D, self.hash_string)

			if self.R[I][D[l]] is not None:
				self.forward()
			else:
				pass				







if __name__ == '__main__':
	n = Node(hashlib.md5("Ankit Solanki".encode()).hexdigest())
	n.print_tables()