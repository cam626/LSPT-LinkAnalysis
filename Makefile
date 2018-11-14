all: main.cpp listener.cpp Sender.cpp
	g++ -o listener.out main.cpp listener.cpp Sender.cpp -no-pie -lpistache -pthread -Wall -g -std=c++11