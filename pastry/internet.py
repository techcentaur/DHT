import random
import numpy as np
from hashlib import md5
from constats import *

class Internet():
	def __init__(self):
		self.nodes = {}
		self.P = np.zeros((N, N))
		self.deleted_nodes = {}

	def get_new_coordinates(self):
		while True:
			x = random.randrange(0, N)
			y = random.randrange(0, N)	
			if self.P[x, y]==0:
				break
		return x, y

	def ping(self, x, y):
		if (x >= 0 and x < N) and (y>=0 and y<N):
			return self.P[x, y]
		return False

	def get_proximity_close_alive_node(self, tup):
		x, y = tup[0], tup[1]
		for size in range(1, N):
			p1 = (x+size, y+size)
			p2 = (x-size, y-size)

			points = []
			points.append(p1)
			points.append(p2)

			for i in range(1, 2*size):
				points.append((p1[0]-i, p1[1]))
				points.append((p1[0], p1[1]-i))

				points.append((p2[0]+i, p2[1]))
				points.append((p2[0], p2[1]+i))

			points.append((x-size, y+size))
			points.append((x+size, y-size))

			for p in points:
				if self.ping(p[0], p[1]):
					return p
		return None

	def alive(self, point, hesh):
		self.P[point[0], point[1]] = 1
		self.deleted_nodes[hesh] = False

	def dead(self, point):
		self.P[point[0], point[1]] = 0
		
		string = str(point[0]) + "+" + str(point[1])
		hesh =  md5(string.encode()).hexdigest()[:hash_size]
		self.deleted_nodes[hesh] = True

	def delete(self):
		key = random.choice(list(self.nodes.keys()))
		pos = self.nodes[key].position

		# delete this node
		self.nodes.pop(key, None)
		self.P[pos[0], pos[1]] = 0
		self.deleted_nodes[key] = True

		for k, v in self.nodes.items():
			v.repair(key, pos)


	def debug(self):
		for v, n in net.nodes.items():
			if not self.deleted_nodes[v]:
				n.print()

net = Internet()