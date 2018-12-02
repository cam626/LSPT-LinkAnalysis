# -*- coding: utf-8 -*- 

import urllib2
from bs4 import BeautifulSoup
from bs4.element import Comment

'''
Text Extractor is a class that performs the text extracting part of text transformation.
    The class takes a path to html file and performs extraction.
'''
class TextExtractor:
    soup = ""

    def __init__(self, html_string):
        self.soup = BeautifulSoup(html_string, features="html.parser")

    '''
    Returns all links in the document (hrefs)
    '''
    def getLinksInDocument(self):
        links = []
        for link in self.soup.find_all('a'):
            if link.has_attr('href'):
                links.append(link['href'].encode('ascii','ignore'))
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
                        header_words.append(word.encode('ascii','ignore').lower())
        return header_words

    '''
    Returns all 'title' words. (not sure what this is)
    '''
    def getTitleListOfWords(self):
        return [item.encode('ascii','ignore').lower() for item in self.soup.title.text.split()]

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
                    words.append(word.encode('ascii','ignore').lower())
        return words

def main():
    path = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<!-- saved from url=(0039)http://www.cs.rpi.edu/~goldsd/index.php -->
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title> David E. Goldschmidt, Ph.D. </title>
    
    <meta name="Author" content="David E. Goldschmidt">
    <meta name="Keywords" content="">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="-1">

    <link rel="stylesheet" type="text/css" href="./example5_files/goldschd.css">
    <link rel="stylesheet" type="text/css" href="./example5_files/goldschd-print.css" media="print">

    <script type="text/javascript" src="./example5_files/goldschd.js"></script>

    <link rel="shortcut icon" href="http://www.cs.rpi.edu/~goldsd/favicon.ico">
  </head>

  <body>
   <div id="all">
    <div id="banner">
    <div id="banner1">
    <div id="banner2">
      <a href="http://www.cs.rpi.edu/~goldsd/index.php"><img src="./example5_files/david-goldschmidt.jpg" width="92" height="108" alt="goldschmidt - David E. Goldschmidt, Ph.D." title="goldschmidt - David E. Goldschmidt, Ph.D." style="border-width: 0;"></a>



      <h1>David E. Goldschmidt, Ph.D.</h1>
      <p>Executive Officer<br>
      <a href="http://www.cs.rpi.edu/" onclick="return w( this.href );">Department of Computer Science</a> at
      <a href="http://www.rpi.edu/" onclick="return w( this.href );">Rensselaer Polytechnic Institute</a></p>


    </div><!-- end banner2 -->
    </div><!-- end banner1 -->
    </div><!-- end banner -->


<div class="colleft">
    <div id="contact">
      <table>
        <tbody><tr>
          <th>My Office:</th>
          <td>Amos Eaton 115</td>
        </tr>
        <tr>
          <th style="padding-top: 5px; vertical-align: top;">My Office Hours:</th>
          <td>Mon/Thu 1:00-2:50PM; Tue 2:30-3:50PM<br><small>(office hours follow the weekly class schedule)</small></td>
        </tr>
        <tr>
          <th>My Email:</th>
          <td><a href="mailto:goldschmidt@gmail.com">goldschmidt@gmail.com</a></td>
        </tr>
      </tbody></table>
    </div><!-- end contact -->


    <div class="lhs">
    <div class="bluebox">
    <div class="bluebox1">
    <div class="bluebox2">
    <div class="bluebox3">
      <h2>Undergraduate Advising</h2>
      <p>
        For undergraduate questions, please review the information at this URL:
        <a href="https://science.rpi.edu/computer-science/programs/undergrad/bs-computerscience" onclick="return w( this.href );">https://science.rpi.edu/computer-science/programs/undergrad/bs-computerscience</a> (or Google "rpi computer science").
      </p>
      <p>
        Contact your assigned academic advisor with questions or concerns;
        he or she is there to help!
        If you do not know who your academic advisor is, you can look in SIS
        (<a href="https://sis.rpi.edu/" onclick="return w( this.href );">https://sis.rpi.edu</a>).
      </p>
      <p>
        Also feel free to visit the School of Science Advising Hub
        (<a href="https://science.rpi.edu/hub" onclick="return w( this.href );">https://science.rpi.edu/hub</a>)
        in J-Rowl&nbsp;1C12 during normal business hours or see Meaghan Potter in AE&nbsp;119 (Mon/Tue/Thu).
      </p>
    </div><!-- end bluebox3 -->
    </div><!-- end bluebox2 -->
    </div><!-- end bluebox1 -->
    </div><!-- end bluebox -->
    </div><!-- end lhs -->



</div><!--end colleft -->



<div class="colright">
    <div class="rhs">
    <div class="greenbox">
    <div class="greenbox1">
    <div class="greenbox2">
    <div class="greenbox3">
    <div class="courses">
      <h2>Courses - Fall 2018</h2>
      <ul>
        <li><!-- crns 61056/63960/63961 -->
          <img src="./example5_files/patterson-sm.jpg" width="62" height="73" alt="Patterson Text" title="Patterson Text">
          CSCI 2500 - Computer Organization<br>
          Tue/Fri 12:00-1:50PM (Sage 3303)<br>
          <a href="https://submitty.cs.rpi.edu/index.php?semester=f18&amp;course=csci2500&amp;component=grading&amp;page=course_materials&amp;action=view_course_materials_page" onclick="return w( this.href );">» course web site (Submitty)</a>
<!--
          |
          <a href="docs/csci2500-f18/csci2500-f18-syllabus.pdf" onclick="return w( this.href );">syllabus</a>
          |
          <a href="docs/csci2500-f18/csci2500-notes-2018-08-31.txt" onclick="return w( this.href );">notes</a>
          |
          <a href="https://www.nytimes.com/2018/06/08/technology/supercomputer-china-us.html" onclick="return w( this.href );">nytimes</a>
-->
        </li>
        <li><!-- crns 64706/64707 -->
          <img src="./example5_files/croft-sm.jpg" width="62" height="80" alt="Croft Text" title="Croft Text">
          CSCI 4460/6460 (CSCI 4963/6963)<br>
          Large-Scale Programming and Testing<br>
          Mon/Thu 10:00-11:50AM (Pitts 4114)<br>
          <a href="https://submitty.cs.rpi.edu/index.php?semester=f18&amp;course=csci4460&amp;component=grading&amp;page=course_materials&amp;action=view_course_materials_page" onclick="return w( this.href );">» course web site (Submitty)</a>
<!--
          |
          <a href="docs/csci4460-f18/csci4460-f18-syllabus.pdf" onclick="return w( this.href );">syllabus</a>
          |
          <a href="docs/csci4460-f18/csci4460-notes-2018-08-30.txt" onclick="return w( this.href );">notes</a>

          <a href="csci2200-s18.php">&raquo; course web site</a>
-->
        </li>
      </ul>
    </div><!-- end courses -->
    </div><!-- end greenbox3 -->
    </div><!-- end greenbox2 -->
    </div><!-- end greenbox1 -->
    </div><!-- end greenbox -->
    </div><!-- end rhs -->


    <div class="rhs">
    <div class="greenbox">
    <div class="greenbox1">
    <div class="greenbox2">
    <div class="greenbox3">
    <div class="courses">
      <h2>RCOS - Fall 2018</h2>
      <ul>
        <li>
          <img src="./example5_files/rcos.png" width="122" height="88" alt="" title="">
          Rensselaer Center for Open Source<br>
          (RCOS)<br>
          Tue/Fri 4:00-5:50PM (DCC 318)<br>
          <a href="http://rcos.io/" onclick="return w( this.href );">» RCOS web site</a><br>
          <a href="http://www.cs.rpi.edu/~goldsd/rcos.php" onclick="return w( this.href );">» required RCOS forms</a><br>
        </li>
      </ul>
<br>
    </div><!-- end courses -->
    </div><!-- end greenbox3 -->
    </div><!-- end greenbox2 -->
    </div><!-- end greenbox1 -->
    </div><!-- end greenbox -->
    </div><!-- end rhs -->



</div><!--end colright -->



   </div><!-- end all -->
  


</body></html>
 """
    te = TextExtractor(path)
    print "Every words : ", te.getListOfWords()
    print "Links : ", te.getLinksInDocument()
    print "Header words : ", te.getHeaderListOfWords()
    print "Title words : ", te.getTitleListOfWords()

if __name__== "__main__":
    main()