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

		net.ping[x, y] = 1 # node alive
		net.nodes[node_hash] = Node(node_hash)

		A = net.get_proximity_close_alive_node(x, y)
		if A:
			A_hash = md5((str(A[0]) + "+" + str(A[1])).encode()).hexdigest()
			res = net.nodes[A_hash].forward(JOIN_MESSAGE, node_hash, first_hop=True)
			if res:
				print("[*] New node inserted @ ({},{})".format(x, y))
				print("[#] Node properties: \n", net.nodes[node_hash].print_tables())

	def lookup(self, msg, key):
		data = next(iter(net.nodes.values)).forward(LOOKUP_MESSAGE, key)
		print("[*] value is: ", data)

	def insert(self, msg, key):
		res = next(iter(net.nodes.values)).forward(msg, key)
		if res:
			print("[*] {}: {} // inserted successfully".format(key, msg))


if __name__ == '__main__':
	n = Network()
	n.add_node()