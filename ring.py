# import matplotlib
# import matplotlib.pyplot as plt

def expanding_ring_algorithm(x, y, size):
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

	# for p in points:
	# 	plt.scatter(p[0], p[1])
	# plt.show()
