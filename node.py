import math
import hashlib

from helper import *
from constats import *
from internet import net

class Node():
	def __init__(self, hash_string, x, y):
		self.hash_string = hash_string
		self.position = (x, y)
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

		self.HT = {} # data structure

	def print_tables(self):
		print("{}".format("-"*40))
		print("[*] Node id: ", self.hash_string)
		print("[*] Position: ", self.position)

		print("[#] Routing Table:")
		for x in self.R:
			print(x)
		print("[#] Neighborhood Set: \n", self.M)
		print("[#] Leaf Set: \n", self.L)
		print("{}".format("-"*40))

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
			elif max_bound is False:
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

	def minimal_key(self, key, __minx=-1, __miny=16, __minimal_key=None):
		for i in range(len(self.L[0]), -1, -1):
			if self.L[0][i]:
				x, y = hex_distance(key, self.L[0][i], absolute=True)
				if (x > __minx) or ((x == __minx) and (y < __miny)):
					__minx, __miny = x, y
					__minimal_key = self.L[0][i]

		for i in range(len(self.L[1])):
			if self.L[1][i]:
				x, y = hex_distance(key, self.L[1][i], absolute=True)
				if (x > __minx) or ((x == __minx) and (y < __miny)):
					__minx, __miny = x, y
					__minimal_key = self.L[1][i]

			
		x, y = hex_distance(self.hash_string, key, absolute=True)
		if (x > __minx) or ((x == __minx) and (y < __miny)):
			__minx, __miny = x, y
			__minimal_key = self.hash_string

		return __minimal_key

	def all_set_minimal(self, key, __minx=-1, __miny=16, __minimal_key=None):
		__minx, __miny = I, Y
		__minimal_key = self.hash_string

		for i in range(I, len(self.R)):
			for j in range(len(self.R[0])):
				if self.R[i][j]:
					x, y = hex_distance(key, self.R[i][j], absolute=True)
					if (x > __minx) or (x==__minx and y < __miny):
						__minx, __miny = x, y
						__minimal_key = self.R[i][j]

		for i in range(len(self.M)):
			x, y = hex_compare(key, self.M[i])
			if x > __minx or (x==__minx and y < __miny):
				__minx, __miny = x, y
				__minimal_key = self.M[i]

		__minimal_key = self.minimal_key(key, __minx=__minx, __miny=__miny, __minimal_key=__minimal_key)
		return __minimal_key

	def forward(self, msg, key, first_hop=False):
		if msg==JOIN_MESSAGE: # for [A-Z] // send R
			(x, y) = hex_distance(key, self.hash_string)
			print("hiss", x, y)
			net.nodes[key].update_R(x, self.R[x])
			
			if first_hop: # for A // send M
				net.nodes[key].update_M(self.M)
			return self.__forward__(msg, key)
		else:
			return self.__forward__(msg, key)

	def __forward__(self, msg, key):
		if self.in_leaf_set(key):
			__key = self.minimal_key(key)
			if __key == self.hash_string:
				if msg==JOIN_MESSAGE:
					net.nodes[key].update_L(self.L)
				elif msg==LOOKUP_MESSAGE:
					return self.HT[key]
				else:
					self.HT[key] = msg
			else:
				return net.nodes[__key].forward(msg, key)
		else:
			(I, y) = hex_distance(key, self.hash_string)

			if self.R[I][D[I]] is not None:
				return net.nodes[self.R[I][key[I]]].forward(msg, key)
			else:
				__key = self.all_set_minimal(key, I, y, self.hash_string)
				if __key == self.hash_string:
					if msg==JOIN_MESSAGE:
						net.nodes[key].update_L(self.L)
					elif msg==LOOKUP_MESSAGE:
						return self.HT[key]
					else:
						self.HT[key] = msg
				else:
					return net.nodes[self.R[I][key[I]]].forward(msg, key)
		return True

if __name__ == '__main__':
	# n = Node(hashlib.md5("Ankit Solanki".encode()).hexdigest())
	# n.print_tables()
	pass