import random
import numpy as np
from constats import *

class Internet():
	def __init__(self):
		self.nodes = {}
		self.P = np.zeros((N, N))

	def get_new_coordinates(self):
		while True:
			x = random.randrange(0, N)
			y = random.randrange(0, N)	
			if self.P[x, y]==0:
				break
		return x, y

	def ping(self, x, y):
		return self.P[x % N , y % N]

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

	def alive(self, point):
		self.P[point[0], point[1]] = 1

	def debug(self):
		for v, n in net.nodes.items():
			n.print_tables()

net = Internet()