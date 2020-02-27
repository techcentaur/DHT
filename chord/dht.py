import random
import hashlib
from chord import Chord


# N = 20
# def get_random_coordinate():
# 	x = random.randrange(0, N)
# 	y = random.randrange(0, N)	
# 	z = random.randrange(0, N)	

# 	return get_hash(str(x) + "+" + str(y) + "+" + str(z))

# def get_hash(string):
# 	return hashlib.md5(string.encode()).hexdigest()


m = 6
chord = Chord(m)

# for i in range(1):
# 	__id = random.randint(0, 100)
# 	chord.join(Node(__id, m))

chord.print()

# chord.fix_fingers()


# for i in range(1, 5):
# 	chord.insert(i, "file{}".format(i))

# for i in range(1, 5)
# 	chord.lookup(i, True)
