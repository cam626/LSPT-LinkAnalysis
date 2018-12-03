# -*- coding: utf-8 -*- 

from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

from bs4 import BeautifulSoup
from bs4.element import Comment
import argparse
import html


'''
Text Extractor is a class that performs the text extracting part of text transformation.
    The class takes a path to html file and performs extraction.
'''
class TextExtractor:
    soup = ""

    def __init__(self, html_string):
        self.soup = BeautifulSoup(html_string, features="html.parser")


    '''
    To string object for the class.
    '''
    def __str__(self):
      output =  'Every Word: {0}\n'.format(self.getListOfWords())
      output += 'Links: {0}\n'.format(self.getLinksInDocument())
      output += 'Header Words: {0}\n'.format(self.getHeaderListOfWords())
      output += 'Title Words: {0}\n'.format(self.getTitleListOfWords())
      return output


    '''
    Returns all links in the document (hrefs)
    '''
    def getLinksInDocument(self):
        links = []
        for link in self.soup.find_all('a'):
            if link.has_attr('href'):
                links.append(html.unescape(link['href']))
        return links

    '''
    Returns all 'header' words (text in h1,h2,h3,h4,h5,etc.) in the document.
    '''
    def getHeaderListOfWords(self):
        header_words = []
        for text in self.soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            if text.text is not None:
                for word in text.text.split():
                    if word.encode('ascii','ignore').lower().isalnum():
                        header_words.append(html.unescape(word).lower())
        return header_words

    '''
    Returns all 'title' words. (not sure what this is)
    '''
    def getTitleListOfWords(self):
        return [html.unescape(item).lower() for item in self.soup.title.text.split()]

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
    Helper function(filter) for getListOfWords().
        It igonores tags or comments that aren't relevant.
    '''
    def tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    '''
    getListOfWords initiates parsing tags within the html 
        and returns valid words found.
    '''
    def getListOfWords(self):
        words = []
        texts = self.soup.findAll(text=True)
        visible_texts = filter(self.tag_visible, texts)  
        for text in visible_texts:
            for word in text.split():
                if word.encode('ascii','ignore').lower().isalnum():
                    words.append(html.unescape(word).lower())
        return words

def main():

    parser = argparse.ArgumentParser()
    
    parser.add_argument('path', help="The path to an html input file")

    args = parser.parse_args()
    path = args.path

    with open(path, 'r') as myfile:
      input_string = myfile.read()

    print(input_string)

    te = TextExtractor(input_string)
    print("Every words : ", te.getListOfWords())
    print("Links : ", te.getLinksInDocument())
    print("Header words : ", te.getHeaderListOfWords())
    print("Title words : ", te.getTitleListOfWords())


if __name__== "__main__":
    main()