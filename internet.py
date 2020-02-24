from constats import *
from helper import expanding_ring_algorithm

class Internet():
	def __init__(self):
		self.nodes = {}

		self.P = np.zeros((N, N))

	@staticmethod
	def get_new_coordinates():
		x = random.randrange(0, N)
		y = random.randrange(0, N)	
		return x, y

	def ping(self, x, y):
		if (x >= 0 and x <= N-1) and (y >= 0 and y <= N-1):
			return self.P[x, y]
		return False

	def get_proximity_close_alive_node(self, x, y):
		for i in range(N):
			points = expanding_ring_algorithm(x, y, i)
			for p in points:
				if self.ping(p[0], p[1]):
					return p
		return None



net = Internet()