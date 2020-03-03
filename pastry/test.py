from hashlib import md5
from internet import net
from constats import *
from network import Network

def get_hash(string):
	return md5(string.encode()).hexdigest()[:hash_size]

def get_random_file_msg(num):
	stuff = []
	for i in range(num):
		stuff.append(("file {}".format(i), get_hash("key {}".format(i))))
	return stuff

def do_tests(n, num_nodes, num_files):
	n.add_nodes(num_nodes)

	# data = get_random_file_msg(num_files)
	# for d in data:
	# 	print("[##] Inserting -> (msg, key): ", d)
	# 	n.insert(d[0], d[1])

	# net.debug()
	# for d in data:
	# 	res = n.lookup(d[1])
	# 	print("[!] LOOKUP: {} -> {} | {}".format(d[1], res, res==d[0]))


	# delete a random element which then tells everyone to repair
	# if their some set/table contained him
	net.delete()


if __name__ == '__main__':
	n = Network(v=True)
	do_tests(n, num_nodes=20, num_files=0)
