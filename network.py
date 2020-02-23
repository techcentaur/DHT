import random
import numpy as np
from hashlib import md5

from helper import expanding_ring_algorithm

b = 2
N = 10

class Network():
	def __init__(self):
		self.internet_dimension = N
		self.ping = np.zeros((N, N))

		self.internet = {}

	def get_new_coordinates(self):
		x = random.randrange(0, self.internet_dimension)
		y = random.randrange(0, self.internet_dimension)	
		return x, y

	def get_closest_node_from(self, node_str):
		x, y = [int(i) for i in node_str.split("+")]

	def add_node(self):
		x, y = self.get_new_coordinates()
		node_hash = md5((str(A[0]) + "+" + str(A[1])).encode()).hexdigest()
		
		A = self.get_A(x, y)

		if A:
			A_hash = md5((str(A[0]) + "+" + str(A[1])).encode()).hexdigest()
			self.internet[A_hash].forward("join", node_hash)

		else: # first node in network
			n = new Node(node_hash)
			
			self.internet[node_hash] = n
			self.ping[x, y] = 1


	def ping_node(self, x, y):
		if (x >= 0 and x <= N-1) and (y >= 0 and y <= N-1):
			return self.ping[x, y]
		return False

	def get_A(self, x, y):
		for i in range(N):
			points = expanding_ring_algorithm(x, y, i)
			for p in points:
				if self.ping_node(p[0], p[1]):
					return p
		return None


if __name__ == '__main__':
	n = Network()
	n.add_node()