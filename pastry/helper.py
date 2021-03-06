from constats import *


def hex_distance(id1, id2):
	for i in range(hash_size):
		if id1[i] != id2[i]:
			return i, abs(hex_map[id1[i]]-hex_map[id2[i]])
	return hash_size, 0

def hex_different_index(id1, id2):
	for i in range(hash_size):
		if id1[i] != id2[i]:
			return i
	return -1

def hex_compare(id1, id2, equality=True):
	"""check if id1 >= id2 if equality=True
			 or id1 > id2 if equality=False
	"""
	if id1==id2:
		if equality:
			return True
		return False

	for i in range(hash_size):
		if id1[i] != id2[i]:
			d = hex_map[id1[i]] - hex_map[id2[i]]
			if d > 0:
				return True
			else:
				return False
	
def distance_metric(point1, point2):
	point = (point2[0]-point1[0], point2[1]-point1[1])
	return max(abs(point[0]), abs(point[1]))

def distance_compare(origin, point1, point2):
	d1 = distance_metric(origin, point1)
	d2 = distance_metric(origin, point2)

	if d1>=d2:
		return True
	return False
