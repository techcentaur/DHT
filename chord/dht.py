import random
import hashlib
from chord import Chord
from node import Node


# def get_hash(string, size=None):
# 	if size:
# 		return hashlib.md5(string.encode()).hexdigest()[:size]
# 	return hashlib.md5(string.encode()).hexdigest()

# def get_mod(key, m):
# 	return hex((int('0x'+key, 16)) % (2**m))

m = 16
chord = Chord(m)

for i in range(100):
	r = random.randint(0, 60240) % (2**m)
# 	hesh = get_hash(str(r), 8)
	print("[*] Adding node | id -> {}".format(r))
	res = chord.join(Node(r, m))
# 	# print("res ", res)
# 	# print("i ", i)


# print("coming here")
chord.fix_fingers()
# keys = []
# for i in range(1, 5):
# 	print("[.] Inserting file: file{}".format(i))
# 	key = random.randint(0, 2**10)
# 	chord.insert(key, "file{}".format(i))
# 	keys.append(key)
# print("coming here too")

chord.print()
# l = int(input())

# chord.leave_node_by_key(l)
# chord.fix_fingers()
# chord.print()
# input()

# for i in range(1, 5):
# 	val = chord.lookup(keys[i-1], True)
# 	print("\n{}->{}".format(keys[i-1], val))

