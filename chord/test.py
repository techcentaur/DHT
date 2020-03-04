"""Here I go testing again"""

import matplotlib
import matplotlib.pyplot as plt

from dht import IntegerTest, HexTest


#==================================
# Writing experiments

def experiment(number, lookup_path=False):
	"""
	number = {}
	keys: 'nodes', 'data', 'queries'
	"""	
	it = IntegerTest(64, 1000000)
	it.setup(number["nodes"])
	it.insert(number["data"])
	print("[?] Executing {} random queries!".format(number["queries"]))

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
	plt.title('Chord | {} nodes - Histogram on Hops'.format(number["nodes"]), fontsize=10)
	plt.ylabel('Number of Queries')


	fig1 = "chord_{}_nodes.svg".format(number["nodes"])
	plt.savefig(fig1)
	print("[+] Histogram saved as: {}".format(fig1))

	it.deletion(int(number["nodes"]/2))
	print("\n[-] Deleted {} random nodes!\n".format(int(number["nodes"]/2)))

	print("[?] Executing {} random queries!".format(number["queries"]))
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
	plt.title('Chord | {} nodes ({} Deleted) - Histogram on Hops'.format(number["nodes"], int(number["nodes"]/2)), fontsize=10)
	plt.xlabel('Number of Hops')
	plt.ylabel('Number of Queries')


	fig2 = "chord_{}_nodes_half_deleted.svg".format(number["nodes"])
	plt.savefig(fig2)
	print("[+] Histogram saved as: {}".format(fig2))


	if lookup_path:
		it.lookup(10, verbose=True)

#==================================

if __name__ == '__main__':
	data1 = {"nodes": 100, "data": 10000, "queries": 100000}

	experiment(data1)

