import math
import hashlib

from helper import *
from constats import *
from internet import net

class Node():
	def __init__(self, node_id, position):
		self.node_id = node_id
		self.position = position
		self.R = [[None for j in range(pow(2, b))] for i in range(hash_size)]
		self.M = [None for x in range(pow(2, b))]
		self.Lmin = [None for x in range(pow(2, b-1))]
		self.Lmax = [None for x in range(pow(2, b-1))] 
		self.HT = {}

	def print(self):
		print("{}".format("-"*40))
		print("[.] Node id: {} | Position {}".format(self.node_id, self.position))
		print("[#] Routing Table:")
		for i in self.R:
			print(i)
		print("[#] Neighborhood Set:", self.M)	
		print("[#] Leaf Set Min:", self.Lmin)
		print("[#] Leaf Set Max:", self.Lmax)
		print("[*] Data: {}".format(self.HT))
		print("{}".format("-"*40))

	def in_leaf_set(self, key):
		if key == self.node_id:
			return True

		_min = self.node_id
		for i in range(len(self.Lmin)):
			if self.Lmin[i] is not None:
				if hex_compare(_min, self.Lmin[i]):
					_min = self.Lmin[i]

		_max = self.node_id
		for i in range(len(self.Lmax)):
			if self.Lmax[i] is not None:
				if hex_compare(self.Lmax[i], _max):
					_max = self.Lmax[i]

		if hex_compare(key, _min) and hex_compare(_max, key):
			return True
		return False

	def update_R(self, r, R):

		self.R[r] = R.copy()

	def update_M(self, close_node):
		ins = (close_node.position, close_node.node_id)
		self.M = close_node.M.copy()

		for i in range(len(self.M)):
			if self.M[i] is None:
				self.M[i] = ins
				return

		_max, _i = -1, -1
		for i in range(len(self.M)):
			d = distance_metric(self.M[i][0], self.position)
			if d > _max:
				_max, _i = d, i

		self.M[_i] = ins

	def update_L(self, Lmin, Lmax, key):
		self.Lmin = Lmin.copy()
		self.Lmax = Lmax.copy()

		if hex_compare(key, self.node_id):
			for i in range(len(self.Lmax)):
				if self.Lmax[i] is None:
					self.Lmax[i] = key
					return

			x, y, j = -1, -1, -1
			for i in range(len(self.Lmax)):
				x1, y1 = hex_distance(self.Lmax[i], self.node_id)
				if (x1 > x) or (x1==x and y1<y):
					x, y, j = x1, y1, i
			
			x1, y1 = hex_distance(key, self.node_id)
			if (x1 > x) or (x1==x and y1<y):
				self.Lmax[j] = key
		else:
			for i in range(len(self.Lmin)):
				if self.Lmin[i] is None:
					self.Lmin[i] = key
					return

			x, y, j = -1, -1, -1
			for i in range(len(self.Lmin)):
				x1, y1 = hex_distance(self.Lmin[i], self.node_id)
				if (x1 > x) or (x1==x and y1<y):
					x, y, j = x1, y1, i
			
			x1, y1 = hex_distance(key, self.node_id)
			if (x1 > x) or (x1==x and y1<y):
				self.Lmin[j] = key

	def transmit_state(self):
		n = self.node_id
		p = self.position
		# M
		for i in range(len(self.M)):
			if self.M[i] is not None:
				net.nodes[self.M[i][1]].update_presence(n, p)

		# R
		for i in range(len(self.R)):
			for j in range(len(self.R[0])):
				if self.R[i][j] is not None:
					net.nodes[self.R[i][j]].update_presence(n, p)

		# L
		for i in range(len(self.Lmin)):
			if self.Lmin[i] is not None:
				net.nodes[self.Lmin[i]].update_presence(n, p)

		for i in range(len(self.Lmax)):
			if self.Lmax[i] is not None:
				net.nodes[self.Lmax[i]].update_presence(n, p)

	def __update__M(self, key, pos):
		for i in range(len(self.M)):
			if self.M[i] is None:
				self.M[i] = (pos, key)
				return

		_max, _i = -1, -1
		for i in range(len(self.M)):
			d = distance_metric(self.M[i][0], self.position)
			if d > _max:
				_max, _i = d, i

		d1 = distance_metric(self.M[_i][0], pos)
		if d > d1:
			self.M[_i] = (pos, key)

	def __update__Lmax(self, key, pos):
		for i in range(len(self.Lmax)):
			if self.Lmax[i] is None:
				self.Lmax[i] = key
				return
		x, y, j = -1, -1, -1
		for i in range(len(self.Lmax)):
			x1, y1 = hex_distance(self.Lmax[i], self.node_id)
			if (x1 > x) or (x1==x and y1<y):
				x, y, j = x1, y1, i
		
		x1, y1 = hex_distance(key, self.node_id)
		if (x1 > x) or (x1==x and y1<y):
			self.Lmax[j] = key

	def __update__Lmin(self, key, pos):
		for i in range(len(self.Lmin)):
			if self.Lmin[i] is None:
				self.Lmin[i] = key
				return
		x, y, j = -1, -1, -1
		for i in range(len(self.Lmin)):
			x1, y1 = hex_distance(self.Lmin[i], self.node_id)
			if (x1 > x) or (x1==x and y1<y):
				x, y, j = x1, y1, i
		
		x1, y1 = hex_distance(key, self.node_id)
		if (x1 > x) or (x1==x and y1<y):
			self.Lmin[j] = key

	def update_presence(self, key, pos):
		# M
		if (pos, key) not in self.M:
			self.__update__M(key, pos)

		# R
		idx = hex_different_index(key, self.node_id)
		if self.R[idx][hex_map[key[idx]]] is None:
			self.R[idx][hex_map[key[idx]]] = key
		if net.nodes[key].R[idx][hex_map[self.node_id[idx]]] is None:
			net.nodes[key].R[idx][hex_map[self.node_id[idx]]] = self.node_id

		# L
		if hex_compare(key, self.node_id):
			if key not in self.Lmax:
				self.__update__Lmax(key, pos)
		else:
			if key not in self.Lmin:
				self.__update__Lmin(key, pos)

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
		return False

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

		# M
		for i in range(len(self.M)):
			if self.M[i] is not None:
				if self.__condition__(self.M[i][1], key, i, self.node_id):
					return self.M[i][1]

		# R
		for i in range(len(self.R)):
			for j in range(len(self.R[0])):
				if self.R[i][j] is not None:
					if self.__condition__(self.R[i][j], key, i, self.node_id):
						return self.R[i][j]

		return self.node_id

	def deliver(self, msg, key):
		if msg == JOIN_MESSAGE:
			net.nodes[key].update_L(self.Lmin, self.Lmax, self.node_id)
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
				return self.deliver(msg, key)
			return net.nodes[k].forward(msg, key)
		else:
			i = hex_different_index(key, self.node_id)
			route = self.R[i][hex_map[key[i]]]

			if route is not None:
				return net.nodes[route].forward(msg, key)

			k = self.all_minimal_key(key)
			if k == self.node_id:	
				return self.deliver(msg, key)
			return net.nodes[k].forward(msg, key)

	def __repair_Lmin__(self, key, pos):
		# for i in range(len(self.Lmin)):
		# 	if self.Lmin[i] is not None:
		# 		pos = net.nodes[self.Lmin[i]].position
		# 		if not net.ping[pos[0], pos[1]]:

		pass

	def __repair_Lmax__(self, key, pos):
		idx = -1

		sort_l = []
		for i in range(len(self.Lmax)):
			if self.Lmax[i] is not None:
				if self.Lmax[i] == key:
					idx = i
				sort_l.append((self.Lmax[i], self.hex_distance(self.position, self.Lmax[i])))
		if idx == -1:
			return

		sort_l.sorted(key=lambda x: x[1])
		pass



	def repair_L(self, key, pos):
		"""
		Repairing the leaf set
		Assume that a leaf L−k fails. (−L/2 < k < 0).
		In this case, the node contacts L−L/2.
		It gets its leaf set and merges it with its leaf set.
		For any new nodes added, it verifies their existence by pinging
		them.
		"""
		self.__repair_Lmin__(key, pos)
		self.__repair_Lmax__(key, pos)

	def repair_R(self, key, pos):
		idx = -1

		for i in range(len(self.R)):
			for j in range(len(self.R[0])):
				if self.R[i][j] is not None:
					if self.R[i][j] == key:
						idx = (i, j)
						break
			else:
				continue
			break

		if idx is -1:
			return

		(i, j) = idx
		flag=False
		for k in range(len(self.R[0])):
			if k != j:
				if self.R[i][k] is not None:
					pos2 = net.nodes[self.R[i][k]].position
					if net.nodes[self.R[i][k]].R[i][j] is not None:
						self.R[i][j] = net.nodes[self.R[i][k]].R[i][j]
						break
		else:
			for k in range(i+1, len(self.R)):
				for l in range(len(self.R[0])):
					if l != j:
						if self.R[k][l] is not None:
							if net.nodes[self.R[k][l]].R[i][j] is not None:
								self.R[i][j] = net.nodes[self.R[k][l]].R[i][j]
								break
				else:
					continue
				break


	def repair_M(self, key, pos):
		idx = -1
		for i in range(len(self.M)):
			if self.M[i] is not None:
				if self.M[i][1] == key:
					idx = i
					break
		if idx==-1:
			return

		sort_M = []
		for i in range(len(self.M)):
			if self.M[i] is not None:
				sort_M.append((i, distance_metric(self.position, self.M[i][0])))
		sort_M.sort(key=lambda x: x[1])

		for j in sort_M:
			tmp = []
			for i in net.nodes[self.M[j[0]][1]].M:
				if (i is not None) and (i[0] != self.position):
					if i not in self.M:
						tmp.append((i, distance_metric(self.position, i[0])))
			tmp.sort(key=lambda x: x[1])

			if len(tmp) > 0:
				self.M[idx] = tmp[0][0]
				break

	def repair(self, key, pos):
		self.repair_M(key, pos)
		self.repair_R(key, pos)
		self.repair_L(key, pos)


