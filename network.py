import random
import numpy as np
from hashlib import md5

from node import Node
from internet import net # global object

from constats import *


class Network():
	def __init__(self):
		pass

	def add_node(self):
		x, y = net.get_new_coordinates()
		node_hash = md5((str(x) + "+" + str(y)).encode()).hexdigest()

		print("[*] Adding new node, x, y are: ", x, y)		

		net.ping[x, y] = 1 # node alive
		net.nodes[node_hash] = Node(node_hash)

		A = net.get_proximity_close_alive_node(x, y)
		if A:
			A_hash = md5((str(A[0]) + "+" + str(A[1])).encode()).hexdigest()
			net.nodes[A_hash].forward(JOIN_MESSAGE, node_hash)

	def lookup(self, key):
		pass

	def insert(self, msg, key):
		next(iter(net.nodes.values)).forward(msg, key)


if __name__ == '__main__':
	n = Network()
	n.add_node()