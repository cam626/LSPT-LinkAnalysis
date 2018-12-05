all: main.cpp listener.cpp Sender.cpp Webgraph.cpp Node.cpp
	g++ -o listener.out *.cpp -no-pie -lpistache -pthread -lcurl -Wall -g -std=c++11