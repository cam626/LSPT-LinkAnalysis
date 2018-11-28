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
    Returns all links in the document (hrefs)
    '''
    def getLinksInDocument(self):
        links = None
        return links

    '''
    Returns all 'header' words (text in h1,h2,h3,h4,h5,etc.) in the document.
    '''
    def getHeaderListOfWords(self):
        return []

    '''
    Returns all 'title' words. (not sure what this is)
    '''
    def getTitleListOfWords(self):
        return []

    '''
    Extract the metadata from the document.
    '''
    def extractMetadata(self):
        metadata = {
            "charset" : None, #metadata field (probably UTF-8)
            'title' : None, #metadata field
            'keywords' : [], #metadata field (don't need to ngram)
            'description' : '', #metadata field
            'docid' : -1 #this is not our job. Just send a -1 (confused by this).
        }
        return metadata


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
    #print te.getListOfWords()

if __name__== "__main__":
    main()