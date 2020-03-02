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
	plt.savefig("fig1.png")
	print("[+] Histogram saved as: ./fig1.png")


	it.deletion(int(number["nodes"]/2))
	print("[---] Deleted {} random nodes [---]".format(int(number["nodes"]/2)))
	# hops = it.lookup(number["queries"])

	# # print avg number of hops
	# s, avg = 0, 0
	# for k, v in hops.items():
	# 	s += v
	# 	avg += k*v
	# avg = avg/s
	# print("[*] Average number of hops: ", avg)

#==================================


data={
	"nodes": 100,
	"data": 1000,
	"queries": 1000
}
experiment(data)