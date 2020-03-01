import random
import hashlib
from chord import Chord
from node import Node


class IntegerTest:
	def __init__(self, m, _range=1000):
		self.m = m
		self.range = _range

	def setup(self, num):
		self.chord = Chord(self.m)

		for i in range(10):
			__id = random.randrange(0, self.range)
			print("[#] Adding node: ", __id)
			self.chord.join(Node(__id, m))

		self.chord.fix_fingers()

	def print(self):
		self.chord.print()

	def insert(self, num, lookup=False):
		keys = []
		for i in range(num):
			print("[.] Inserting file: `file{}`".format(i))
			key = random.randint(0, self.range)
			self.chord.insert(key, "`file{}`".format(i))
			keys.append(key)


		if lookup:
			for i in range(num):
				val = chord.lookup(keys[i], True)
				print("Lookup of: {} -> got: {}".format(keys[i], val))

	def self.deletion(self):
		pass


def 


def get_hash(string, size=None):
	if size:
		return hashlib.md5(string.encode()).hexdigest()[:int(size)]
	return hashlib.md5(string.encode()).hexdigest()

m = 32
chord = Chord(m)
	
for i in range(10):
	r = get_hash(str(random.randrange(0, 102400)), size=(m/4))
	print("[*] Adding node | id -> {}".format(r))
	res = chord.join(Node(r, m))
	print("res ", res)


# print("coming here")
chord.fix_fingers()
chord.print()

