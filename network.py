from hashlib import md5

from node import Node
from internet import net # global object

from constats import *


class Network():
	def __init__(self, v):
		self.v = v
		pass

	def add_node(self):
		x, y = net.get_new_coordinates()
		node_hash = md5((str(x) + "+" + str(y)).encode()).hexdigest()

		if self.v:
			print("{}".format("="*40))
			print("[*] Trying to add {} | {}".format((x, y), node_hash))

		net.P[x, y] = 1 # node alive
		net.nodes[node_hash] = Node(node_hash, x, y)

		A = net.get_proximity_close_alive_node((x, y))
		if self.v:
			print("[*] Proximity node: ", A)
		res = False
		if A:
			A_hash = md5((str(A[0]) + "+" + str(A[1])).encode()).hexdigest()
			res = net.nodes[A_hash].forward(JOIN_MESSAGE, node_hash, first_hop=True)
		else:
			# first node in network
			res = True
			pass

		net.nodes[node_hash].transmit_state()

		# if res:
		# 	if self.v:
		# 		print("[*] New node inserted @ ({},{})".format(x, y))
		# 		print("[#] Node properties: \n")
		# 		for v, n in net.nodes.items():
		# 			n.print_tables()

	def lookup(self, key, msg=LOOKUP_MESSAGE):
		data = next(iter(net.nodes.values())).forward(msg, key)
		print("[*] value is: ", data)
		return data

	def insert(self, msg, key):
		res = (next(iter(net.nodes.values()))).forward(msg, key)
		if res:
			print("[*] {}: {} // inserted successfully".format(key, msg))

	def add_nodes(self, num=1):
		for i in range(num):
			self.add_node()

def get_hash(string):
	return md5(string.encode()).hexdigest()

def get_random_file_msg(num):
	stuff = []
	for i in range(num):
		stuff.append(("file {}".format(i), get_hash("key {}".format(i))))
	return stuff

if __name__ == '__main__':
	import sys
	v = int(sys.argv[1])
	n = Network(v)
	n.add_nodes(4)

	data = get_random_file_msg(5)
	for d in data:
		print("[##] Inserting: ", d)
		n.insert(d[0], d[1])

	# for v, n1 in net.nodes.items():
	# 	n1.print_tables()

	for d in data:
		res = n.lookup(d[1])
		print("LOOKUP: ", res, d[0])