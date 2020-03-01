def dist_hex(hex1, hex2):
	if hex1==hex2:
		return 0
	sub = (int('0x'+hex2, 16) - int('0x'+hex1, 16))
	if (int('0x'+hex2, 16) > int('0x'+hex1, 16)):
		return hex(sub)
	return hex((2**10 + sub) % (2**10))
