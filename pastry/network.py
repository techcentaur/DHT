from hashlib import md5

from node import Node
from internet import net # global object

from constats import *
from test import (do_tests, get_hash)


class Network():
	def __init__(self, v):
		self.v = v

	def add_node(self):
		x, y = net.get_new_coordinates()
		node_hash = get_hash(str(x) + "+" + str(y))

		if self.v:
			print("[!] Adding {} | {}".format((x, y), node_hash))

		net.alive((x, y))
		net.nodes[node_hash] = Node(node_hash, (x, y))

		close_node = net.get_proximity_close_alive_node((x, y))
		if self.v:
			print("[*] Proximity node: ", close_node)

		if close_node:
			close_hash = get_hash(str(close_node[0]) + "+" + str(close_node[1]))
			net.nodes[close_hash].forward(JOIN_MESSAGE, node_hash, first_hop=True)
		else:
			pass # first node in network

		net.debug()
		input()
		net.nodes[node_hash].transmit_state()
		net.debug()
		input()


	def lookup(self, key, msg=LOOKUP_MESSAGE):
		data = next(iter(net.nodes.values())).forward(msg, key)
		return data

	def insert(self, msg, key):
		print("everything works till here")
		res = (next(iter(net.nodes.values()))).forward(msg, key)

	def add_nodes(self, num=1):
		for i in range(num):
			self.add_node()


if __name__ == '__main__':
	verbose=1
	n = Network(verbose)
	do_tests(n, num_nodes=5, num_file_insert=5)



