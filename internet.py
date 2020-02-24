import random
import numpy as np

from constats import *
from helper import expanding_ring_algorithm

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
		if (x >= 0 and x <= N-1) and (y >= 0 and y <= N-1):
			return self.P[x, y]
		return False

	def get_proximity_close_alive_node(self, tup):
		for i in range(1, N):
			points = expanding_ring_algorithm(tup, i)
			for p in points:
				if self.ping(p[0], p[1]):
					return p
		return None



net = Internet()
