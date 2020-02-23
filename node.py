b = 2
N = 100
import hashlib
import math

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

	@staticmethod
	def id_compare(id1, id2):
		hex_map = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15}
		idx = None
		for i in range(32):
			if id1[i] != id2[i]:
				idx = i
				return (idx, hex_map[id1[idx]]-hex_map[id2[idx]])
		return (idx, None)

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

	@staticmethod
	def common_prefix(K, node_id):
		for i in range(32):
			if K[i] != node_id[i]:
				return i
		return -1

	def routing(self, msg, key):
		if len(key) is not 128:
			D = hashlib.md5(key.encode()).hexdigest() 

		# comapring with leaf set
		# self.forward_if_in_leaf_set_range(D)
		t = False
		if t:
			pass
		else:
			I = self.common_prefix(D, self.hash_string)
			if I == -1:
				print("[!] Error")
			if self.R[I][D[l]] is not None:
				self.forward()
			else:
				pass				







if __name__ == '__main__':
	n = Node(hashlib.md5("Ankit Solanki".encode()).hexdigest())
	n.print_tables()