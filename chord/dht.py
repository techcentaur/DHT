import random
import hashlib
from chord import Chord
from node import Node

# N = 20
# def get_random_coordinate():
# 	x = random.randrange(0, N)
# 	y = random.randrange(0, N)	
# 	z = random.randrange(0, N)	

# 	return get_hash(str(x) + "+" + str(y) + "+" + str(z))

# def get_hash(string):
# 	return hashlib.md5(string.encode()).hexdigest()


m = 10
chord = Chord(m)

for i in range(10):
	__id = random.randint(0, 10240) % 2**10
	print("[*] Adding node | id -> {}".format(__id))
	chord.join(Node(__id, m))

chord.fix_fingers()

keys = []
for i in range(1, 5):
	print("[.] Inserting file: file{}".format(i))
	key = random.randint(0, 2**10)
	chord.insert(key, "file{}".format(i))
	keys.append(key)

chord.print()
l = int(input())

chord.leave_node_by_key(l)
chord.fix_fingers()
chord.print()
input()

for i in range(1, 5):
	val = chord.lookup(keys[i-1], True)
	print("\n{}->{}".format(keys[i-1], val))

