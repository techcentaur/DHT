import random
import numpy as np
from hashlib import md5

from ring import expanding_ring_algorithm

b = 2
N = 10

class Network():
	def __init__(self):
		self.internet_dimension = N
		self.ping = np.zeros((N, N))

	def get_new_coordinates(self):
		x = random.randrange(0, self.internet_dimension)
		y = random.randrange(0, self.internet_dimension)	
		return x, y

	def get_closest_node_from(self, node_str):
		x, y = [int(i) for i in node_str.split("+")]

	def add_node(self):
		x, y = self.get_new_coordinates()
		
		node_str = str(x) + "+" + str(y)
		hash_string = md5(node_str.encode()).hexdigest()

		self.get_A(hash_string)



if __name__ == '__main__':
	n = Network()
	n.add_node()