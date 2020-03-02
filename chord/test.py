"""Here I go testing again"""

import matplotlib
import matplotlib.pyplot as plt

from dht import IntegerTest, HexTest


#==================================
# Writing experiments

def experiment(number):
	"""
	number = {}
	keys: 'nodes', 'data', 'queries'
	"""	
	it = IntegerTest(40, 10000)
	it.setup(number["nodes"])
	it.insert(number["data"])
	hops = it.lookup(number["queries"])
	print("\t[HOPS]: ", hops)

	# print avg number of hops
	s, avg = 0, 0
	for k, v in hops.items():
		s += v
		avg += k*v
	avg = avg/s
	print("[*] Average number of hops: ", avg)

	# histogram for distribution of hops
	plt.bar(hops.keys(), hops.values(), color='g')
	plt.title('Chord | {} nodes and {} data-points - Histogram on Hops'.format(number["nodes"], number["data"]))
	plt.xlabel('Number of Hops')
	plt.ylabel('Number of Queries')


	fig1 = "{}_nodes.png".format(number["nodes"])
	plt.savefig(fig1)
	print("[+] Histogram saved as: {}".format(fig1))

	it.deletion(int(number["nodes"]/2))
	print("\n[-] Deleted {} random nodes!\n".format(int(number["nodes"]/2)))

	hops = it.lookup(number["queries"])
	print("\t[HOPS]: ", hops)

	# print avg number of hops
	s, avg = 0, 0
	for k, v in hops.items():
		s += v
		avg += k*v
	avg = avg/s
	print("[*] Average number of hops: ", avg)

	plt.clf()
	plt.bar(hops.keys(), hops.values(), color='g')
	plt.title('Chord | {} nodes ({} DELETED) and {} data-points - Histogram on Hops'.format(number["nodes"], int(number["nodes"]/2), number["data"]))
	plt.xlabel('Number of Hops')
	plt.ylabel('Number of Queries')


	fig2 = "{}_nodes_half_deleted.png".format(number["nodes"])
	plt.savefig(fig2)
	print("[+] Histogram saved as: {}".format(fig2))


#==================================

test1 = {"nodes": 10, "data": 1000, "queries": 10000}
test2 = {"nodes": 20, "data": 1000, "queries": 10000}
test3 = {"nodes": 30, "data": 1000, "queries": 10000}
# data1 = {"nodes": 100, "data": 10000, "queries": 1000000}
# data2 = {"nodes": 500, "data": 10000, "queries": 1000000}
# data3 = {"nodes": 1000, "data": 10000, "queries": 1000000}

experiment(data)