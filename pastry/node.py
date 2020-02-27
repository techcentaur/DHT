import math
import hashlib

from helper import *
from constats import *
from internet import net

class Node():
	def __init__(self, node_id, position):
		self.node_id = node_id
		self.position = position
		self.R = [None for j in range(pow(2, b)) for i in range(hash_size)]
		self.M = [None for x in range(pow(2, b+1))]
		self.Lmin = [None for x in range(pow(2, b-1))]
		self.Lmax = [None for x in range(pow(2, b-1))] 
		self.HT = {}

	def print_tables(self):
		print("{}".format("-"*40))
		print("[.] Node id: {} | Position {}".format(self.node_id, self.position))
		print("[#] Routing Table:", self.R)
		print("[#] Neighborhood Set:", self.M)
		print("[#] Leaf Set Min:", self.Lmin)
		print("[#] Leaf Set Max:", self.Lmax)
		print("[*] Data: {}".format(self.HT))
		print("{}".format("-"*40))

	def in_leaf_set(self, key):
		if key == self.node_id:
			return True

		_min = self.node_id
		for i in self.Lmin:
			if i is not None:
				if hex_compare(_min, self.Lmin[i]):
					_min = self.Lmin[i]

		_max = self.node_id
		for i in self.Lmax:
			if i is not None:
				if hex_compare(self.Lmax[i], _max):
					_max = self.Lmax[i]

		if hex_compare(key, _min) and hex_compare(_max, key):
			return True
		return False

	def update_R_entry(self, key):
		x = hex_different_index(key, self.node_id)
		if x is -1:
			return
		if self.R[x][hex_map[key[x]]] is None:
			self.R[x][hex_map[key[x]]] = key

	def update_R(self, r, R):
		self.R[r] = R.copy()

	def update_M(self, close_node):
		ins = (close_node.position, close_node.node_id)
		self.M = close_node.M.copy()

		for i in range(len(self.M)):
			if self.M[i] is None:
				self.M[i] = ins

		_max = -1
		_i = -1
		for i in range(len(self.M)):
			d = distance_metric(self.M[i][0], self.position)
			if d > _max:
				_max, _i = d, i

		self.M[i] = ins


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

	def minimal_key(self, key):
		x, y = hex_distance(key, self.node_id)
		k = self.node_id

		for i in range(len(self.Lmin)):
			if self.Lmin[i] is not None:
				a, b = hex_distance(self.Lmin[i], key)
				if (a > x) or (a==x and b < y):
					x, y = a, b
					k = self.Lmin[i]

		for i in range(len(self.Lmax)):
			if self.Lmax[i] is not None:
				a, b = hex_distance(self.Lmax[i], key)
				if (a > x) or (a==x and b < y):
					x, y = a, b
					k = self.Lmax[i]
		return k

	@staticmethod
	def __condition__(T, K, I, nodeId):
		j = hex_different_index(T, K)
		a, b = hex_distance(T, K)
		x, y = hex_distance(nodeId, K)

		if (j>=I) and ((a > x) or (a==x and b < y)):
			return True
		else False


	def all_minimal_key(self, key):
		i = hex_different_index(key, self.node_id)

		# L
		for i in range(len(self.Lmin)):
			if self.Lmin[i] is not None:
				if self.__condition__(self.Lmin[i], key, i, self.node_id):
					return self.Lmin[i]

		for i in range(len(self.Lmax)):
			if self.Lmax[i] is not None:
				if self.__condition__(self.Lmax[i], key, i, self.node_id):
					return self.Lmax[i]

		# R
		for i in range(self.R):
			for j in range(self.R[0]):
				if self.R[i][j] is not None:
					if self.__condition__(self.R[i][j], key, i, self.node_id):
						return self.R[i][j]

		# M
		for i in range(len(self.M)):
			if self.M[i] is not None:
				if self.__condition__(self.M[i][1], key, i, self.node_id):
					return self.M[i][1]

		return self.node_id


	def deliver(self, msg, key):
		if msg == JOIN_MESSAGE:
			net.nodes[key].update_L(self.L, self.node_id)
			return 1
		elif msg==LOOKUP_MESSAGE:
			return self.HT[key]
		else:
			self.HT[key] = msg
			return 1

	def forward(self, msg, key):
		if msg==JOIN_MESSAGE:
			x = hex_different_index(key, self.node_id)
			net.nodes[key].update_R(x, self.R[x])
		return self.__forward__(msg, key)

	def __forward__(self, msg, key):
		if self.in_leaf_set(key):
			k = self.minimal_key(key)
			if k == self.node_id:
				return deliver(msg, key)
			return net.nodes[k].forward(msg, key)
		else:
			i = hex_different_index(key, self.node_id)
			route = self.R[i][hex_map[key[i]]]

			if route is not None:
				return net.nodes[route].forward(msg, key)

			k = self.all_minimal_key(key)
			if k == self.node_id:
				return deliver(msg, key)
			return net.nodes[k].forward(msg, key)

		print("**************this can't possible print")
