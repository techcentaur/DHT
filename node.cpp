#include <iostream>
#include <vector>

using namespace std;

#define B 4

struct cell
{
char val[128];	
};

class node
{
private:
	vector<vector<cell>> routingTable;
	vector<cell> neighborhoodTable;
	vector<cell> leafSet;

public:
	
	
	
};