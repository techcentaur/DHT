from hashlib import md5

def get_hash(string):
	return md5(string.encode()).hexdigest()

def get_random_file_msg(num):
	stuff = []
	for i in range(num):
		stuff.append(("file {}".format(i), get_hash("key {}".format(i))))
	return stuff

def do_tests(n, num_nodes, num_file_insert):
	n.add_nodes(num_nodes)

	data = get_random_file_msg(num_file_insert)
	for d in data:
		print("[##] Inserting -> (msg, key): ", d)
		n.insert(d[0], d[1])

	# for v, n1 in net.nodes.items():
	# 	n1.print_tables()

	for d in data:
		res = n.lookup(d[1])
		print("[!] LOOKUP: {} -> {} | {}".format(d[1], res, res==d[0]))
