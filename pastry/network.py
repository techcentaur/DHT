from hashlib import md5

from node import Node
from internet import net # global object
import random
from constats import *

def get_hash(string):
	return md5(string.encode()).hexdigest()[:hash_size]

class Network():
	def __init__(self, v):
		self.v = v

	def add_node(self):
		x, y = net.get_new_coordinates()
		node_hash = get_hash(str(x) + "+" + str(y))

		if self.v:
			print("[!] Adding {} | {}".format((x, y), node_hash))

		net.alive((x, y), node_hash)
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

	def lookup_n_queries(self, points, num=1):
		hops = {}
		for i in range(num):
			rand = random.randrange(1, points)
			h = self.lookup(get_hash("key {}".format(rand)))
			if h in hops:
				hops[h] += 1
			else:
				hops[h] = 1
		return hops

	def lookup(self, key, msg=LOOKUP_MESSAGE):
		hops = next(iter(net.nodes.values())).forward(msg, key)
		return hops

	def insert(self, msg, key):
		res = (next(iter(net.nodes.values()))).forward(msg, key)

	def add_nodes(self, num=1):
		for i in range(num):
			self.add_node()
