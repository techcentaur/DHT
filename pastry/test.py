from hashlib import md5
from internet import net
from constats import *
from network import Network

import matplotlib
import matplotlib.pyplot as plt

def get_hash(string):
	return md5(string.encode()).hexdigest()[:hash_size]

def get_random_file_msg(num):
	stuff = []
	for i in range(num):
		stuff.append(("file {}".format(i), get_hash("key {}".format(i))))
	return stuff

def do_tests(n, num_nodes, num_files):
	n.add_nodes(num_nodes)
	net.debug()
	# for d in data:
	# 	res = n.lookup(d[1])
	# 	print("[!] LOOKUP: {} -> {} | {}".format(d[1], res, res==d[0]))


	# delete a random element which then tells everyone to repair
	# if their some set/table contained him
	net.delete()
	net.debug()


class Experiment:
	def __init__(self, v=False):
		self.n = Network(v)
		pass

	def avg_hops(self, hops):
		# get avg number of hops
		s, avg = 0, 0
		for k, v in hops.items():
			s += v
			avg += k*v
		avg = avg/s
		return avg

	def save_histogram(self, hops, number, prefix1, prefix2):
		plt.clf()
		plt.bar(hops.keys(), hops.values(), color='b')
		plt.title('Pastry | {} nodes and {} data-points {}- Histogram on Hops'.format(number["nodes"], number["data"], prefix2))
		plt.xlabel('Number of Hops')
		plt.ylabel('Number of Queries')

		fig1 = "{}_{}_nodes.png".format(prefix1, number["nodes"])
		plt.savefig(fig1)
		print("[+] Histogram saved as: {}".format(fig1))


	def run(self, number, delete=False):
		if delete is False:
			print("[?] Adding {} nodes to pastry!".format(number["nodes"]))
			self.n.add_nodes(number["nodes"])
			print("[+] Successfully added {} nodes!\n".format(number["nodes"]))


			print("[?] Trying to add {} data-points in the pastry...".format(number["data"]))
			data = get_random_file_msg(number["data"])
			for d in data:
				self.n.insert(d[0], d[1])
			print("[+] Successfully added {} data-points!\n".format(number["data"]))


			print("[#] Looking up {} random queries".format(number["queries"]))
			hops = self.n.lookup_n_queries(number["data"], number["queries"])
			print("\t[HOPS]: ", hops)

			avg = self.avg_hops(hops)
			print("[*] Average number of hops: ", avg)

			self.save_histogram(hops, number, "pastry", "")

		else:
			print("[?] Adding {} nodes to pastry!".format(number["nodes"]))
			self.n.add_nodes(number["nodes"])
			print("[+] Successfully added {} nodes!\n".format(number["nodes"]))

			print("[?] Deleting {} nodes from pastry!".format(int(number["nodes"]/2)))
			net.delete(int(number["nodes"]/2))
			print("[+] Successfully deleted {} nodes!\n".format(int(number["nodes"]/2)))

			print("[?] Trying to add {} data-points in the pastry...".format(number["data"]))
			data = get_random_file_msg(number["data"])
			for d in data:
				self.n.insert(d[0], d[1])
			print("[+] Successfully added {} data-points!\n".format(number["data"]))

			print("[#] Looking up {} random queries".format(number["queries"]))
			hops = self.n.lookup_n_queries(number["data"], number["queries"])
			print("\t[HOPS]: ", hops)

			avg = self.avg_hops(hops)
			print("[*] Average number of hops: ", avg)

			self.save_histogram(hops, number, "pastry_half_deleted_nodes_", "(Deleted Half Nodes)")



if __name__ == '__main__':
	n = Network(v=False)

	data = {"nodes": 100, "data": 1000, "queries": 10000}

	exp = Experiment()
	exp.run(data)

	print("\n" + "="*30)
	print("[!] Internet Rebooted! [!]")
	print("="*30 + "\n")
	net.restart_internet()

	exp.run(data, delete=True)

