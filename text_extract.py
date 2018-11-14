import xml.etree.ElementTree as ET

class TextExtractor:
    htmlPath = ''
    tree = ET.ElementTree()
    root = ET.Element('')

    def __init__(self, htmlPath):
        self.htmlPath = htmlPath
        self.tree = ET.parse(self.htmlPath)
        self.root = self.tree.getroot()

    #Takes base_prices.json, find price-determining options for each product and save the order
    def getWords(self, text, words):
        if text is not None:
            for word in text.split():
                   words.append(word)      

    def getListOfWords(self):
        words = []
        self.parseNodes(self.root, words)
        return words

    '''
    parseNodes takes current node and list of words for input
        then for 
    '''
    def parseNodes(self, node, words):
        self.getWords(node.text, words)
        for child in node:
            self.parseNodes(child, words)
        self.getWords(node.tail, words)

def main():
    path = 'Examples/example1.html'
    te = TextExtractor(path)
    print te.getListOfWords()

if __name__== "__main__":
    main()