import random
import hashlib
from chord import Chord

N = 20
def get_random_coordinate():
	x = random.randrange(0, N)
	y = random.randrange(0, N)	
	z = random.randrange(0, N)	

	return get_hash(str(x) + "+" + str(y) + "+" + str(z))

def get_hash(string):
	return hashlib.md5(string.encode()).hexdigest()

m = 6
chord = Chord(m)