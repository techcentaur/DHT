"""Here I go testing again"""

from dht import IntegerTest, HexTest

ht = IntegerTest(8, 10000)
ht.setup(5)
ht.insert(5)
ht.print()
ht.lookup()
