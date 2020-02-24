# class A:
# 	def __init__(self):
# 		self.val = 5

# 	def f(self, b):
# 		print(self.val)

# class B:
# 	def f(self, a):
# 		self.a = a
# 		self.a.val = 6

# a = A()
# print(a.val)
# b = B()
# b.f(a)
# print(b.a.val)
# print(a.val)


import hashlib
from operator import itemgetter, attrgetter
S = []
s = "solanki is a bad boy duh"
for i in s.split():
	S.append(hashlib.md5(i.encode()).hexdigest())

print(S)

l=[(3,-2),(5,2), (4, -2), (5,9), (5,-10), (3,1)]
b = sorted(l, key=lambda x: x[1])
b = sorted(b, key=lambda x: x[0])
print(l)
print(b)

l = [[None, None, None], [None, None, None]]
for idx, j in enumerate(b):
	if j[1] < 0:
		for i in range(len(l[0])-1, -1, -1):
			if l[0][i] is None:
				l[0][i] = S[idx]
				break
	else:
		for i in range(len(l[1])):
			if l[1][i] is None:
				l[1][i] = S[idx]
				break

print(l)