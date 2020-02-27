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
			net.nodes[node_hash].update_M(net.nodes[close_hash])
			net.nodes[close_hash].forward(JOIN_MESSAGE, node_hash)
		else:
			pass # first node in network

		# net.nodes[node_hash].print()
		net.nodes[node_hash].transmit_state()


	def lookup(self, key, msg=LOOKUP_MESSAGE):
		data = next(iter(net.nodes.values())).forward(msg, key)
		return data

	def insert(self, msg, key):
		res = (next(iter(net.nodes.values()))).forward(msg, key)

	def add_nodes(self, num=1):
		for i in range(num):
			self.add_node()


if __name__ == '__main__':
	n = Network(v=True)
	do_tests(n, num_nodes=100, num_file_insert=5)



