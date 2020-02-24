# import matplotlib
# import matplotlib.pyplot as plt

def expanding_ring_algorithm(x, y, size):
	"""return list(points) in expanding squares with radius = size"""

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
	# for p in points:
	# 	plt.scatter(p[0], p[1])
	# plt.show()

	return points

hex_map = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15}

def hex_distance(id1, id2, num_bytes=32, absolute=False):
	""" return (x, y)
		at xth index the character is different
		and y is the distance of xth characters (+ve when id1 > id2)
	"""
	
	if id1==id2:
		return (32, 0)

	for i in range(num_bytes):
		if id1[i] != id2[i]:
			if absolute:
				return (i, abs(hex_map[id1[i]]-hex_map[id2[i]]))
			return (i, hex_map[id1[i]]-hex_map[id2[i]])

def hex_compare(id1, id2, equality=True, none_check=False, num_bytes=32):
	"""check if id1 >= id2 if equality=True
			 or id1 > id2 if equality=False
	"""

	if none_check:
		if (not id2) or (not id2):
			return False

	if equality:
		if id1==id2:
			return True
		for i in range(num_bytes):
			if id1[i] != id2[i]:
				d = hex_map[id1[i]] - hex_map[id2[i]]
				if d >= 0:
					return True
				else:
					return False
	else:
		if id1==id2:
			return False
		for i in range(num_bytes):
			if id1[i] != id2[i]:
				d = hex_map[id1[i]] - hex_map[id2[i]]
				if d > 0:
					return True
				else:
					return False
