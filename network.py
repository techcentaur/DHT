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

		print("{}".format("="*40))
		print("[*] Trying to add {} | {}".format((x, y), node_hash))

		net.P[x, y] = 1 # node alive
		net.nodes[node_hash] = Node(node_hash, x, y)

		A = net.get_proximity_close_alive_node((x, y))
		res = False
		if A:
			A_hash = md5((str(A[0]) + "+" + str(A[1])).encode()).hexdigest()
			res = net.nodes[A_hash].forward(JOIN_MESSAGE, node_hash, first_hop=True)
		else:
			# first node in network
			res = True
			pass

		# transmit state
		net.nodes[node_hash].transmit_state()

		if res:
			print("[*] New node inserted @ ({},{})".format(x, y))
			print("[#] Node properties: \n")
			for v, n in net.nodes.items():
				n.print_tables()

	def lookup(self, msg, key):
		data = next(iter(net.nodes.values)).forward(LOOKUP_MESSAGE, key)
		print("[*] value is: ", data)

	def insert(self, msg, key):
		res = next(iter(net.nodes.values)).forward(msg, key)
		if res:
			print("[*] {}: {} // inserted successfully".format(key, msg))

	def add_nodes(self, num=1):
		for i in range(num):
			self.add_node()

if __name__ == '__main__':
	n = Network()
	n.add_nodes(2)