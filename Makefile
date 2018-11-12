all: main.cpp listener.cpp
	g++ -o listener.out main.cpp listener.cpp -no-pie -lpistache -pthread -Wall -g -std=c++11