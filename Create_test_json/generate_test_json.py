import json
import random
# -*- coding: utf-8 -*


def createJson(startLetter, webSize):
    j = {}
    j["Head"] = "www." + startLetter + ".com"
    j["Tails"] = []
    for i in range(webSize):
        j["Tails"].append("www." + chr(ord("a")+random.randrange(0, 25, 1))  + chr(ord("a")+random.randrange(0, 25, 1)) + ".com")
    # print(j)
    with open(("test_" + startLetter + ".json"),"w") as f:
        json.dump(j,f)


def createJson2(startLetter, webSize):
    j = {}
    j["Head"] = "www." + startLetter + ".com"
    j["Tails"] = []
    for i in range(webSize):
        j["Tails"].append("www."+ chr(ord("a")+random.randrange(0, 25, 1))  + chr(ord("a")+random.randrange(0, 25, 1))+ chr(ord("a")+random.randrange(0, 25, 1)) + ".com")
    # print(j)
    with open(("test_" + startLetter + ".json"),"w") as f:
        json.dump(j,f)


def main():
    # startLetter1 = "a"
    # while ord(startLetter1) <= ord("z"):
    #     startLetter2 = "a"
    #     while ord(startLetter2) <= ord("z"):
    #         startLetter = startLetter1+startLetter2
    #         createJson2(startLetter, 10)
    #         print ("curl -XPUT -H" + "\'" + "Content-Type: application/json" "\' " + "localhost:9080/family_person?pretty -d@test_" + startLetter1 + startLetter2 +".json")
    #         startLetter2 = chr(ord(startLetter2)+1)
    #     startLetter1 = chr(ord(startLetter1)+1)

    startLetter1 = "a"
    while ord(startLetter1) <= ord("z"):
        createJson(startLetter1, 1024)
        print ("curl -XPUT -H" + "\'" + "Content-Type: application/json" "\' " + "localhost:9080/family_person?pretty -d@test_" + startLetter1 + ".json")
        startLetter1 = chr(ord(startLetter1)+1)

if __name__ == "__main__":
    main()