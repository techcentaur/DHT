import random
import hashlib
from chord import Chord
from node import Node


class IntegerTest:
	def __init__(self, m, _range=1000):
		self.m = m
		self.range = _range
		self.nodes_ids = []

	def setup(self, num=10):
		self.chord = Chord(self.m, dist="integer")

		print("[*] Adding {} nodes!".format(num))
		for i in range(num):
			res = -1
			while res != 1:
				__id = random.randrange(0, self.range) % (2**self.m)
				# print("[#] Adding node: ", __id)
				res = self.chord.join(Node(__id, self.m))
			self.nodes_ids.append(__id)
		self.chord.fix_fingers()

	def print(self):
		self.chord.print()

	def insert(self, num, lookup=False):
		keys = []
		print("[#] Inserting {} random data points!".format(num))
		for i in range(num):
			key = random.randint(0, self.range) %(2**self.m)
			# print("[.] Inserting file: {} -> `file{}`".format(key, i))
			self.chord.insert(key, "`file{}`".format(i))
			keys.append(key)
		self.keys = keys

		if lookup:
			self.lookup()

	def lookup(self, num, verbose=False):
		hops = {}
		for i in range(num):
			j = random.randrange(0, len(self.keys))
			val = self.chord.lookup(self.keys[j], verbose)
			# print("Lookup of: {} -> got: {}".format("file{}".format(i), val))
			if val in hops:
				hops[val] += 1
			else:
				hops[val] = 1
		return hops

	def deletion(self, num=1):
		for i in range(num):
			self.chord.leave_node_by_key(self.nodes_ids[i])
			self.chord.fix_fingers()

class HexTest:
	def __init__(self, m, _range=1000):
		self.m = m
		self.range = _range

	@staticmethod
	def get_hash(string):
		return hashlib.md5(string.encode()).hexdigest()

	def setup(self, num=10):
		self.chord = Chord(self.m, dist="hex")

		for i in range(num):
			h1 = random.randrange(0, self.range)
			h2 = random.randrange(0, self.range)
			hesh = self.get_hash(str(h1) + "-" + str(h2))[:int(self.m/4)]

			print("[#] Adding node: ", hesh)
			self.chord.join(Node(hesh, self.m))

		self.chord.fix_fingers()

	def print(self):
		self.chord.print()

	def insert(self, num, lookup=False):
		keys = []
		for i in range(num):
			print("[.] Inserting file: `file{}`".format(i))
			
			h1 = random.randrange(0, self.range)
			h2 = random.randrange(0, self.range)
			hesh = get_hash(str(h1) + "-" + str(h2))[:int(self.m/4)]

			self.chord.insert(hesh, "`file{}`".format(i))
			keys.append(hesh)

		if lookup:
			for i in range(num):
				val = chord.lookup(keys[i], True)
				print("Lookup of: {} -> got: {}".format(keys[i], val))

	def deletion(self):
		pass

