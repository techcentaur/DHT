import math
import hashlib

from helper import *
from constats import *
from internet import net

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
		# assume leaf set property on how it has been filled
		# in min: from right -> left
		# in max: from left -> right

		self.HT = {}

	def print_tables(self):
		print("[*] Node id: ", self.hash_string)
		print("[#] Routing Table:")
		for x in self.R:
			print(x)
		print("[#] Neighborhood Set: \n", self.M)
		print("[#] Leaf Set: \n", self.L)

	def in_leaf_set(self, D):
		min_bound = False if self.L[0][-1] else None
		max_bound = False if self.L[1][0] else None

		print(self.L)
		print("[!] Bounds: min, max: ", min_bound, max_bound)
		
		for i in range(len(self.L[0])-1, -1, -1):
			if hex_compare(D, self.L[0][i], equality=True, none_check=True):
				min_bound = True

		for i in range(len(self.L[1])-1, -1, -1):
			if hex_compare(self.L[1][i], D, equality=True, none_check=True):
				max_bound = True

		if min_bound:
			if max_bound:
				return True
			elif max_bound is False:
				return False
			else:
				if hex_compare(self.hash_string, D, equality=False, none_check=False):
					return True
				return False
		elif min_bound is False:
			return False
		else:
			if max_bound:
				if hex_compare(D, self.hash_string, equality=False, none_check=False):
					return True
				return False
			elif max_bound if False:
				return False
			else:
				return False

	def update_R(self, row, data):
		self.R[row] = data

	def update_M(self, M):
		self.M = M

	def update_L(self, L):
		leaves = []
		for i in L[0]:
			if i:
				leaves.append(hex_distance(self.hash_string, i), i)
		for i in L[1]:
			if i:
				leaves.append(hex_distance(self.hash_string, i), i)

		l0, l1 = [], []
		for i in leaves:
			if i[1] < 0:
				l0.append(i)
			else:
				l1.append(i)

		l0.sort(key=lambda x: x[0])
		l1.sort(key=lambda x: x[0], reverse=True)

		self.L[0][len(l0)*-1:] = l0
		self.L[1][:len(l1)] = l1

	def forward(self, msg, key, hops=0):
		if len(key) is not 32:
			key = hashlib.md5(key.encode()).hexdigest() 

		if msg.upper()==JOIN_MESSAGE: # for [A-Z]
			(x, y) = hex_distance(key, self.hash_string)
			net.nodes[key].update_R(x, self.R[x])
			
			if hops==0: # for A // send M
				net.nodes[key].update_M(self.M)

			r = self.routing(msg, key, hops)
			if not r: # for Z // sends L
				net.nodes[key].update_L(self.L)
				return True
		else:
			pass

	def minimal_key(self, key):
		# don't need list // can keep minimal yet

		minimal = []
		for i in range(len(self.L[0]), -1, -1):
			if self.L[0][i]:
				x, y = hex_distance(key, self.L[0][i])
				# if x==32:
					# this is the node
				minimal.append(((x, -1*abs(y)), (0, i)))
		for i in range(len(self.L[1])):
			if self.L[1][i]:
				minimal.append(((x, -1*abs(y)), (1, i)))

		minimal.sort(key=lambda x: x[0])
		
		k = minimal[-1][1]
		return self.L[k[0]][k[1]]

	def all_set_minimal(self, key, I, Y):
		# L set i already searched right?

		__minx, __miny = I, Y

		for i in range(I, len(self.R)):
			for j in range(len(self.R[0])):
				if self.R[i][j]:
					x, y = hex_compare(key, self.R[i][j], absolute=True)
					if (x > __minx or (x==__minx and y < __miny)) and ():
						minimal = self.R[i][j]
						return minimal

		for i in range(len(self.M)):
			x, y = hex_compare(key, self.M[i])
			if x > __minx or (x==__minx and y < __miny):
				minimal = self.R[i][j]
				return minimal

		return None



	def routing(self, msg, key, hops=0):
		is_routed = False
		if self.in_leaf_set(key):
			__key = self.minimal_key(key)
			is_routed = net.nodes[__key].forward(msg, key, hops+1)
		else:
			(I, y) = hex_distance(key, self.hash_string)

			if self.R[I][D[I]] is not None:
				is_routed = net.nodes[self.R[I][key[I]]].forward(msg, key, hops+1)
			else:
				__key = self.all_set_minimal(key, I, y)
				if __key:
					is_routed = net.nodes[self.R[I][key[I]]].forward(msg, key, hops+1)
				else:
					pass

		return is_routed


if __name__ == '__main__':
	n = Node(hashlib.md5("Ankit Solanki".encode()).hexdigest())
	n.print_tables()