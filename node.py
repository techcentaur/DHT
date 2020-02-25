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

		# math.ceil(math.log(N, pow(2, b)))
		for i in range(32):
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
		for idx, x in enumerate(self.R):
			p = []
			for i in range(len(x)):
				if x[i]:
					p.append((i, x[i]))
			if len(p) != 0:
				print(idx, " -> ", p)
		print("[#] Neighborhood Set:")
		for i in self.M:
			if i:
				print(i, end=' ')
		print("\n[#] Leaf Set:")
		print("Min:", )
		for i in self.L[0]:
			if i is not None:
					print(i, )
		print("Max:", )
		for i in self.L[1]:
			if i is not None:
					print(i, )
		
		print("{}".format("-"*40))

	def in_leaf_set(self, D):
		if self.L[0][-1]:
			min_bound = False
		else:
			min_bound = None

		if self.L[1][0]:
			max_bound = False
		else:
			max_bound = None
		
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

	def update_R_entry(self, key):
		x, y = hex_distance(key, self.hash_string)
		if self.R[x][hex_map[key[x]]] is None:
			self.R[x][hex_map[key[x]]] = key

	def update_R(self, row, data):

		self.R[row] = data.copy()

	def update_M(self, M, pos, key):

		self.M = [(pos, key)] + M[1:]
		self.update_R_entry(key)

	def update_L(self, L, key):
		if key==self.hash_string:
			return
		if hex_compare(key, self.hash_string):
			self.update_R_entry(key)

			big = [key]
			for i in range(len(L[0])-1, -1, -1):
				if L[0][i]:
					if hex_compare(L[0][i], self.hash_string):
						big.append(L[0][i])
					else:
						self.L[0][len(self.L[0])-i:] = L[0][:i]
			big.reverse()
			size = len(big)
			if size >= len(self.L[1]):
				self.L[1]=big[:len(self.L[1])]
			else:
				self.L[1][:size] = big[:]
				for i in range(size, len(self.L[1])):
					self.L[1][i] = L[1][i-size]
		else:
			less = [key]
			for i in range(len(L[1])):
				if L[1][i]:
					if hex_compare(self.hash_string, L[1][i]):
						less.append(L[1][i])
					else:
						self.L[1][:len(self.L[1])-i] = L[1][i:]
			size = len(less)
			if size >= len(self.L[1]):
				self.L[0]=less[size-len(self.L[1]):]
			else:
				self.L[0][len(self.L[0])-size:] = less[:]
				for i in range(len(self.L[0])-size-1, -1, -1):
					self.L[0][i] = L[0][i+size]


	def whatf(self, L, key):
		leaves = [(hex_distance(key, self.hash_string), key)]

		for i in L[0]:
			if i:
				leaves.append((hex_distance(i, self.hash_string), i))
		for i in L[1]:
			if i:
				leaves.append((hex_distance(i, self.hash_string), i))

		l0, l1 = [], []
		for i in leaves:
			if i[0][1] < 0:
				l0.append(i)
			else:
				l1.append(i)

		l0.sort(key=lambda x: x[0])
		l1.sort(key=lambda x: x[0], reverse=True)

		self.L[0][len(self.L[0])+len(l0)*-1:] = [x[1] for x in l0]
		self.L[1][:len(l1)] = [x[1] for x in l1]

	def transmit_state(self):
		# to  M
		for i in range(len(self.M)):
			if self.M[i] is not None:
				net.nodes[self.M[i][1]].update_presence_of(self.hash_string, self.position)

		# to R
		for i in range(len(self.R)):
			for j in range(len(self.R[0])):
				if self.R[i][j] is not None:
					net.nodes[self.R[i][j]].update_presence_of(self.hash_string, self.position)

		# to L
		for i in range(len(self.L[0])):
			if self.L[0][i] is not None:
				net.nodes[self.L[0][i]].update_presence_of(self.hash_string, self.position)

		for i in range(len(self.L[1])):
			if self.L[1][i] is not None:
				net.nodes[self.L[1][i]].update_presence_of(self.hash_string, self.position)

	def update_presence_of(self, new_key, new_pos):
		if new_key==self.hash_string:
			return

		(x, y) = hex_distance(new_key, self.hash_string)

		# M
		if (new_pos, new_key) not in self.M:
			for i in range(len(self.M)):
				if self.M[i] is not None:
					if distance_compare(self.position, self.M[i][0], new_pos):
						l = len(self.M)
						self.M[i:i] = [(new_pos, new_key)]
						self.M = self.M[:l]
						break
				else:
					self.M[i] = (new_pos, new_key)
					break

		# L
		if y>=0: # in L max
			if new_key not in self.L[1]:
				for i in range(len(self.L[1])):
					if self.L[1][i] is not None:
						if hex_compare(self.L[1][i], new_key, equality=False):
							l = len(self.L[1])
							self.L[1][i:i] = [new_key]
							self.L[1] = self.L[1][:l]
							break
					else:
						self.L[1][i] = new_key
						break
		else: # in L min
			if new_key not in self.L[0]:
				for i in range(len(self.L[0])-1, -1, -1):
					if self.L[0][i] is not None:
						if hex_compare(new_key, self.L[0][i], equality=False):
							l = len(self.L[0])
							self.L[0][i:i] = [new_key]
							self.L[0] = self.L[0][l*-1:]
							break
					else:
						self.L[0][i] = new_key
						break

		# R
		self.R[x][hex_map[new_key[x]]] = new_key

	def minimal_key(self, key, __minx=-1, __miny=16, __minimal_key=None):
		for i in range(len(self.L[0])-1, -1, -1):
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
		for i in range(__minx, len(self.R)):
			for j in range(len(self.R[0])):
				if self.R[i][j]:
					x, y = hex_distance(key, self.R[i][j], absolute=True)
					if (x > __minx) or (x==__minx and y < __miny):
						__minx, __miny = x, y
						__minimal_key = self.R[i][j]

		for i in range(len(self.M)):
			if self.M[i]:
				x, y = hex_distance(key, self.M[i][1])
				if x > __minx or (x==__minx and y < __miny):
					__minx, __miny = x, y
					__minimal_key = self.M[i][1]

		__minimal_key = self.minimal_key(key, __minx, __miny, __minimal_key)
		return __minimal_key

	def forward(self, msg, key, first_hop=False):
		if msg==JOIN_MESSAGE: # for [A-Z] // send R
			
			(x, y) = hex_distance(key, self.hash_string)
			net.nodes[key].update_R(x, self.R[x])
			
			if first_hop: # for A // send M
				net.nodes[key].update_M(self.M, self.position, self.hash_string)
			return self.__forward__(msg, key)
		else:
			return self.__forward__(msg, key)

	def __forward__(self, msg, key):
		if self.in_leaf_set(key):
			__key = self.minimal_key(key)
			if __key == self.hash_string:
				if msg==JOIN_MESSAGE:
					net.nodes[key].update_L(self.L, self.hash_string)
				elif msg==LOOKUP_MESSAGE:
					return self.HT[key]
				else:
					self.HT[key] = msg
			else:
				return net.nodes[__key].forward(msg, key)
		else:
			(I, y) = hex_distance(key, self.hash_string)

			if self.R[I][hex_map[key[I]]] is not None:
				return net.nodes[self.R[I][hex_map[key[I]]]].forward(msg, key)
			else:
				__key = self.all_set_minimal(key, I, y, self.hash_string)
				if __key == self.hash_string:
					if msg==JOIN_MESSAGE:
						net.nodes[key].update_L(self.L, self.hash_string)
					elif msg==LOOKUP_MESSAGE:
						return self.HT[key]
					else:
						self.HT[key] = msg
				else:
					return net.nodes[__key].forward(msg, key)
		return True

if __name__ == '__main__':
	# n = Node(hashlib.md5("Ankit Solanki".encode()).hexdigest())
	# n.print_tables()
	pass