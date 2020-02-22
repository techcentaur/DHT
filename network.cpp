#include <openssl/md5.h>
#include<bits/stdc++.h>

using namespace std;

#define internetDimension 1000
#define hashSize = 128

class network
{
private:
	tuple<int, int> assignCoordinate(){
		int x = rand() % internetDimension;
		int y = rand() % internetDimension;

		return make_tuple(x, y);
	} 
public:
	network(){
	}
	vector<vector<bool>> ping;

	void addInTable(){
		// recieve from nodes and update tables
	}

	void addNode(){
		tuple<int, int> coord;
		coord = this->assignCoordinate();

		string str = to_string(get<0>(coord)) + "+" + to_string(get<1>(coord));

		unsigned char hash[128];
		MD5((unsigned  char*)str.c_str(), str.size(),  hash);

		cout<<hash<<endl;
		cout<<get<0>(coord)<<" "<<get<1>(coord)<<endl;

		// n = getClosestNode(c);
		// giveMeTable(n)
	}
};

int main(){
	network n = network();
	srand(time(NULL));
	n.addNode();
	return 0;
}