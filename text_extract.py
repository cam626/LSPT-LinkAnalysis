import xml.etree.ElementTree as ET

'''
Text Extractor is a class that performs the text extracting part of text transformation.
    The class takes a path to html file and performs extraction.
'''
class TextExtractor:
    htmlPath = ''
    tree = ET.ElementTree()
    root = ET.Element('')

    def __init__(self, htmlPath):
        self.htmlPath = htmlPath
        self.tree = ET.parse(self.htmlPath)
        self.root = self.tree.getroot()

    '''
    getListOfWords initiates parsing tags within the html 
        and returns valid words found.
    '''
    def getListOfWords(self):
        words = []
        self.parseNodes(self.root, words)
        return words

    '''
    parseNodes recursively takes current node and list of words for input
        then strip valid words that get added to words list.
    '''
    def parseNodes(self, node, words):
        self.getWords(node.text, words)
        for child in node:
            self.parseNodes(child, words)
        self.getWords(node.tail, words)

    '''
    getWords takes text(or tail) attribute from each tag
        and add them to words lists.
    '''
    def getWords(self, text, words):
        if text is not None:
            for word in text.split():
                   words.append(word)      

def main():
    path = 'Examples/example1.html'
    te = TextExtractor(path)
    print te.getListOfWords()

if __name__== "__main__":
    main()