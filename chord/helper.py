def dist_hex(hex1, hex2):
	if hex1==hex2:
		return 0
	sub = (int('0x'+hex2, 16) - int('0x'+hex1, 16))
	if (int('0x'+hex2, 16) > int('0x'+hex1, 16)):
		return hex(sub)
	return hex((2**10 + sub) % (2**10))

a=1
b=1000

hex1 = hex(int(a))
hex2 = hex(int(b))

print(hex1, hex2)
ret = dist_hex(hex1[2:], hex2[2:])
print(ret)