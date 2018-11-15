All: Webgraph.cpp Node.cpp Test_Webgraph.cpp
	g++ *.cpp -o test.out -Wall -g -std=c++11

all: main.cpp listener.cpp Sender.cpp
	g++ -o listener.out main.cpp listener.cpp Sender.cpp -no-pie -lpistache -pthread -Wall -g -std=c++11