hex_map = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15}

def expanding_ring_algorithm(tup, size):
	"""return list(points) in expanding squares with radius = size"""
	x, y = tup

	p1 = (x+size, y+size)
	p2 = (x-size, y-size)

	points = []
	points.append(p1)
	points.append(p2)

	for i in range(1, 2*size):
		points.append((p1[0]-i, p1[1]))
		points.append((p1[0], p1[1]-i))

		points.append((p2[0]+i, p2[1]))
		points.append((p2[0], p2[1]+i))


	points.append((x-size, y+size))
	points.append((x+size, y-size))

	return points


def hex_distance(id1, id2, absolute=False):
	""" return (x, y)
		at xth index i at which the character is different between strings
		and y is the distance of xth characters (+ve when id1 > id2)
	"""
	
	for i in range(32):
		if id1[i] != id2[i]:
			if absolute:
				return (i, abs(hex_map[id1[i]]-hex_map[id2[i]]))
			return (i, hex_map[id1[i]]-hex_map[id2[i]])
	return (-1, -1)

def hex_different_index(id1, id2):
	"""return: the index of first different character in id1 and id2"""
	
	for i in range(32):
		if id1[i] != id2[i]:
			return i
	return -1


def hex_compare(id1, id2, equality=True, none_check=False):
	"""check if id1 >= id2 if equality=True
			 or id1 > id2 if equality=False
	"""

	# if none_check:
	# 	if (id1 is None) or (id2 is None):
	# 		return False

	if equality:
		if id1==id2:
			return True
		for i in range(32):
			if id1[i] != id2[i]:
				d = hex_map[id1[i]] - hex_map[id2[i]]
				if d >= 0:
					return True
				else:
					return False
	else:
		if id1==id2:
			return False
		for i in range(32):
			if id1[i] != id2[i]:
				d = hex_map[id1[i]] - hex_map[id2[i]]
				if d > 0:
					return True
				else:
					return False

def distance_metric(origin, point):
	point = (point[0]-origin[0], point[1]-origin[1])
	return max(abs(point[0]), abs(point[1]))

def distance_compare(origin, point1, point2):
	d1 = distance_metric(origin, point1)
	d2 = distance_metric(origin, point2)

	if d1>=d2:
		return True
	return False
