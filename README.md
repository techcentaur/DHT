# DHT
Distributed Hash Tables (DHT) Implementation // Pastry + Chord

## Pastry

Pastry is a scalable distributed object location and routing substrate for wide-area peer-to-peer applications. Pastry performs application-level routing and object location in a potentially very large overlay network of nodes connected via the Internet.

[wiki](https://en.wikipedia.org/wiki/Pastry_(DHT)) [research-paper](http://rowstron.azurewebsites.net/PAST/pastry.pdf)

#### What is the analogy in simulating pastry on computer

- Usually, say we hash ip-address and perform an application-level routing. But if we do same here, say we generate random IP, we would be hard to distinguish between physical proximity and hash-code distance, calculations increase and things get difficult.
- So, what we can think of internet it as 2-D grid of points, and each coordinate `hash(10,4)` would be our hash-id. Now a good question is, in actual internet with the help of ip-address any node can ping any other ip-address, for getting the same usage of coordiate, I create a 2-D matrix, where pinging means checking if co-ordinate exists.
- Below code from `internet.py` will depict this (pretty self-explanatory):

```python3

class Internet():
	def __init__(self):
		self.nodes = {}
		self.P = [[0 for i in range(N)] for i in range(N)]
		self.deleted_nodes = {}
		self.del_nodes = 0

	def get_new_coordinates(self):
		while True:
			x = random.randrange(0, N)
			y = random.randrange(0, N)	
			if self.P[x][y]==0:
				break
		return x, y

	def ping(self, x, y):
		if (x >= 0 and x < N) and (y>=0 and y<N):
			return self.P[x][y]
		return False
```

#### Directory Structure
- internet.py # the internet
- helper.py # distance and comparison functions between hex hash-ids
- network.py # this is the interface to add node, put something, get something (can be made available at every node in real)
- node.py # node structure
- test.py # i needed this to submit my assignment in required form
- constants.py # few global constants 

#### How to run

1. Go into `test.py`
2. Change `data` dictionary with suitable parameters
    For e.g:	data = {"nodes": 100, "data": 10000, "queries": 1000000} (random data points and queries)
3. Run `python3 ./pastry/test.py`

#### Example run

For `data = {"nodes": 100, "data": 10000, "queries": 1000000}`, deleting half nodes after first testing and then test again.

```console
[?] Adding 100 nodes to pastry!
[+] Successfully added 100 nodes!
[+] Successfully added 10000 data-points!
[#] Looking up 1000000 random queries
	[HOPS]:  {2: 531243, 3: 218033, 4: 87736, 1: 135580, 5: 25939, 6: 1469}
[*] Average number of hops:  2.341618

[?] Deleting 50 nodes from pastry!
[+] Successfully deleted 50 nodes!

[#] Looking up 1000000 random queries
	[HOPS]:  {1: 124825, 3: 196035, 2: 639745, 4: 39395}
[*] Average number of hops:  2.15
```

## Chord
Chord is a protocol and algorithm for a peer-to-peer distributed hash table. A distributed hash table stores key-value pairs by assigning keys to different computers (known as "nodes"); a node will store the values for all the keys for which it is responsible.

[Wiki](https://en.wikipedia.org/wiki/Chord_(peer-to-peer)) [research-paper](https://pdos.csail.mit.edu/papers/ton:chord/paper-ton.pdf)

Chord is super intuitive, here are some cool slides (with easy psuedo code snippets) [LINK](http://www.cse.iitd.ac.in/~srsarangi/courses/col_819_2020/docs/chord.pdf)

#### Cool Code Snippet

Here is how to iterate through chord DHT if you want
```python3
	def fix_fingers(self):
		self.first_node.update_finger_table(self)

		__next = self.first_node.finger_table[0]
		while __next != self.first_node:
			__next.update_finger_table(self)
			__next = __next.finger_table[0] # this gives me the next node
```

Remove a node
```python3
	def leave(self, bye_node):
		# put all that this node contains in the next one
		for key, value in bye_node.HT.items():
			bye_node.finger_table[0].HT[key] = value

		if bye_node.finger_table[0] == bye_node:
			self.first_node = None
		else:
			# change variables on the nodes in front of me and behind me
			bye_node.predecessor.finger_table[0] = bye_node.finger_table[0]
			bye_node.finger_table[0].predecessor = bye_node.predecessor

			# update if it is the first node in ring (as per my coding assumption)
			if self.first_node == bye_node:
				self.first_node = bye_node.finger_table[0]
```

#### Directory Structure

'node.py': node class of a chord (in reality should be execute at one computer)
'chord.py': all main functions to handle dht chord
'test.py': testing chord // use this to know how to run my code
'helper.py': helper functions
'dht.py': this was required by my assignment

#### How to run

1. Go into `./chord/test.py`
2. Change `data` dictionary with suitable parameters
    For e.g:	data = {"nodes": 100, "data": 10000, "queries": 1000000} (random data points and queries)
3. Run `python3 test.py`

#### Example run

For `data = {"nodes": 100, "data": 10000, "queries": 1000000}`, deleting half nodes after first testing and then test again.

```console
[*] Adding 100 nodes!
[#] Inserting 10000 random data points!
[?] Executing 1000000 random queries!
	[HOPS]:  {3: 165673, 5: 310696, 1: 20238, 4: 328732, 2: 73870, 6: 73895, 7: 26896}
[*] Average number of hops:  4.165047

[-] Deleted 50 random nodes!

[?] Executing 1000000 random queries!
	[HOPS]:  {5: 269675, 3: 378284, 4: 284619, 2: 38771, 1: 20139, 6: 8512}
[*] Average number of hops:  3.770456
```


### Issues

Raise issues if you have any.