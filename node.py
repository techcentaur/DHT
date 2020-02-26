import math
import hashlib

from helper import *
from constats import *
from internet import net

class Node():
	def __init__(self, node_id, position):
		self.node_id = node_id
		self.position = position
		self.R = []

		# math.ceil(math.log(N, pow(2, b)))
		for i in range(32):
			self.R.append([None for j in range(pow(2, b))])

		self.M = [None for x in range(pow(2, b+1))]
		# [min, max]
		self.L = [[None for x in range(pow(2, b-1))], [None for x in range(pow(2, b-1))]] 
		# assume leaf set property on how it has been filled
		# in min: <------------ # in max ---------------->

		self.HT = {} # data structure

	def print_tables(self):
		print("{}".format("-"*40))
		print("[.] Node id: {} | Position {}".format(self.node_id, self.position))

		print("[#] Routing Table:")
		for idx, x in enumerate(self.R):
			p = []
			for i in range(len(x)):
				if x[i]:
					p.append((i, x[i]))
			if len(p) != 0:
				print(idx, " -> ", p, end=' | ')
		print("[#] Neighborhood Set:")
		for i in self.M:
			if i:
				print(i, end=' ')
		print("\n[#] Leaf Set:")
		print("Min: ", end=' ')
		for i in self.L[0]:
			if i is not None:
					print(i, end=' ')
		print("Max:", end=' ')
		for i in self.L[1]:
			if i is not None:
					print(i, end=' ')
		
		print("[*] Data: {}".format(self.HT))
		print("{}".format("-"*40))

	def in_leaf_set(self, key):
		if hex_compare(key, self.node_id, equality=False):
			# self.node_id << key << self.L[1]
			for i in range(len(self.L[1])):
				if self.L[1][i]:
					if hex_compare(self.L[1][i], key, equality=True):
						return True
		else:
			# self.L[0] << key << self.node_id
			for i in range(len(self.L[0])-1, -1, -1):
				if self.L[0][i]:
					if hex_compare(key, self.L[0][i], equality=True):
						return True
		return False

	def update_R_entry(self, key):
		x, y = hex_distance(key, self.node_id)
		if self.R[x][hex_map[key[x]]] is None:
			self.R[x][hex_map[key[x]]] = key

	def update_R(self, row, data):

		self.R[row] = data.copy()

	def update_M(self, M, pos, key):

		self.M = [(pos, key)] + M[1:]
		self.update_R_entry(key)

	def update_L(self, L, key):
		if hex_compare(key, self.node_id):
			self.update_R_entry(key)

			big = [key]
			for i in range(len(L[0])-1, -1, -1):
				if L[0][i]:
					if hex_compare(L[0][i], self.node_id):
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
					if hex_compare(self.node_id, L[1][i]):
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

	def transmit_state(self):
		# to  M
		for i in range(len(self.M)):
			if self.M[i] is not None:
				net.nodes[self.M[i][1]].update_presence_of(self.node_id, self.position)

		# to R
		for i in range(len(self.R)):
			for j in range(len(self.R[0])):
				if self.R[i][j] is not None:
					net.nodes[self.R[i][j]].update_presence_of(self.node_id, self.position)

		# to L
		for i in range(len(self.L[0])):
			if self.L[0][i] is not None:
				net.nodes[self.L[0][i]].update_presence_of(self.node_id, self.position)

		for i in range(len(self.L[1])):
			if self.L[1][i] is not None:
				net.nodes[self.L[1][i]].update_presence_of(self.node_id, self.position)

	def update_presence_of(self, new_key, new_pos):
		if new_key==self.node_id:
			return

		(x, y) = hex_distance(new_key, self.node_id)

		# M
		if (new_pos, new_key) not in self.M:
			for i in range(len(self.M)):
				if self.M[i] is not None:
					if distance_compare(self.position, self.M[i][0], new_pos):
						tmp = (new_pos, new_key)
						for j in range(i, len(self.M)):
							tmp1 = self.M[j]
							self.M[j] = tmp
							tmp = tmp1
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
							tmp = new_key
							for j in range(i, len(self.L[1])):
								tmp1 = self.L[1][j]
								self.L[1][j] =  tmp
								tmp = tmp1
							break
					else:
						self.L[1][i] = new_key
						break
		else: # in L min
			if new_key not in self.L[0]:
				for i in range(len(self.L[0])-1, -1, -1):
					if self.L[0][i] is not None:
						if hex_compare(new_key, self.L[0][i], equality=False):
							tmp = new_key
							for j in range(i, -1, -1):
								tmp1 = self.L[0][j]
								self.L[0][j] = tmp
								tmp = tmp1		
							break
					else:
						self.L[0][i] = new_key
						break

		# R
		self.R[x][hex_map[new_key[x]]] = new_key
		net.nodes[new_key].R[x][hex_map[self.node_id[x]]] = self.node_id

	def minimal_key(self, key, __minx=-1, __miny=16, __minimal_key=None):
		for i in range(len(self.L[0])-1, -1, -1):
			if self.L[0][i]:
				x, y = hex_distance(key, self.L[0][i], absolute=True)
				if x == -1:
					return self.L[0][i]
				if (x > __minx) or ((x == __minx) and (y < __miny)):
					__minx, __miny = x, y
					__minimal_key = self.L[0][i]

		for i in range(len(self.L[1])):
			if self.L[1][i]:
				x, y = hex_distance(key, self.L[1][i], absolute=True)
				if x == -1:
					return self.L[1][i]
				if (x > __minx) or ((x == __minx) and (y < __miny)):
					__minx, __miny = x, y
					__minimal_key = self.L[1][i]

			
		x, y = hex_distance(self.node_id, key, absolute=True)
		if x is -1:
			return self.node_id
		if (x > __minx) or ((x == __minx) and (y < __miny)):
			__minx, __miny = x, y
			__minimal_key = self.node_id

		return __minimal_key

	def all_set_minimal(self, key, __minx=-1, __miny=16, __minimal_key=None):
		for i in range(__minx, len(self.R)):
			for j in range(len(self.R[0])):
				if self.R[i][j]:
					x, y = hex_distance(key, self.R[i][j], absolute=True)
					if x is -1:
						return self.R[i][j]
					if (x > __minx) or (x==__minx and y < __miny):
						__minx, __miny = x, y
						__minimal_key = self.R[i][j]

		for i in range(len(self.M)):
			if self.M[i]:
				x, y = hex_distance(key, self.M[i][1])
				if x is -1:
					return self.M[i][1]
				if x > __minx or (x==__minx and y < __miny):
					__minx, __miny = x, y
					__minimal_key = self.M[i][1]

		__minimal_key = self.minimal_key(key, __minx, __miny, __minimal_key)
		return __minimal_key

	def forward(self, msg, key, first_hop=False):
		if msg==JOIN_MESSAGE: # for [A-Z] // send R
			x = hex_different_index(key, self.node_id)
			net.nodes[key].update_R(x, self.R[x])
			
			if first_hop: # for A // send M
				net.nodes[key].update_M(self.M, self.position, self.node_id)
			res = self.__forward__(msg, key)
			print(msg, key)
			return res
		else:
			return self.__forward__(msg, key)

	def __forward__(self, msg, key):
		if self.in_leaf_set(key):
			__key = self.minimal_key(key)

			if __key == self.node_id:
				if msg==JOIN_MESSAGE:
					net.nodes[key].update_L(self.L, self.node_id)
				elif msg==LOOKUP_MESSAGE:
					return self.HT[key]
				else:
					self.HT[key] = msg
			else:
				return net.nodes[__key].forward(msg, key)
		else:
			(I, y) = hex_distance(key, self.node_id, absolute=True)

			__route = self.R[I][hex_map[key[I]]]
			if __route is not None:
				return net.nodes[__route].forward(msg, key)
			else:
				__key = self.all_set_minimal(key, I, y, self.node_id)
				if __key == self.node_id:
					if msg==JOIN_MESSAGE:
						net.nodes[key].update_L(self.L, self.node_id)
					elif msg==LOOKUP_MESSAGE:
						return self.HT[key]
					else:
						self.HT[key] = msg
				else:
					res = net.nodes[__key].forward(msg, key)
					print(msg, key)
					return res
		return True

if __name__ == '__main__':
	# n = Node(hashlib.md5("Ankit Solanki".encode()).hexdigest())
	# n.print_tables()
	pass