from text_extract import TextExtractor
import ngrams
import json
import compare
import os
import unittest
import argparse

################################################
#
# UTILITY FUNCTIONS
#
################################################

'''
Given a path to an html file, open it and return its
contents as a string
'''
def openHtmlFileAsString(file_path):
  with open(file_path, 'r') as infile:
    input_string = infile.read()
  return input_string

'''
Given a path to an txt file, open it and return its
contents as a list of words
'''
def openTxtFileAsList(file_path):
    with open(file_path, 'r') as infile:
      words = infile.read().split()
    return words

'''
Given a path to an txt file, open it and return its
contents as a list of words
'''
def openTxtFileAsString(file_path):
    with open(file_path, 'r') as infile:
      words = infile.read()
    return words

'''
Given a path to an json file, open it and return its
contents as a dict
'''
def openJsonFile(file_path):
  with open(file_path) as data_file:    
    data = json.load(data_file)
  return data

################################################
#
# TEXT EXTRACTOR TESTS
#
################################################
class TextExtractorTests(unittest.TestCase):
  
  def test1(self):
    test_file = 'example1'
    print(" BEGINNING TEXT EXTRACTION TESTS")
    print("Testing {0}.html".format(test_file))

    html_file = os.path.join('Examples','html_files','{0}.html'.format(test_file))
    expected_output_file = os.path.join('Examples','expected_html_output','{0}.txt'.format(test_file))

    te = TextExtractor(openHtmlFileAsString(html_file))
    expected_output = openTxtFileAsString(expected_output_file)

    self.assertEqual(str(te),expected_output)

  def test2(self):
    test_file = 'example2'
    print(" Testing {0}.html".format(test_file))
    
    html_file = os.path.join('Examples','html_files','{0}.html'.format(test_file))
    expected_output_file = os.path.join('Examples','expected_html_output','{0}.txt'.format(test_file))

    te = TextExtractor(openHtmlFileAsString(html_file))
    expected_output = openTxtFileAsString(expected_output_file)

    self.assertEqual(str(te),expected_output)

  def test3(self):
    test_file = 'example3'
    print(" Testing {0}.html".format(test_file))
    
    html_file = os.path.join('Examples','html_files','{0}.html'.format(test_file))
    expected_output_file = os.path.join('Examples','expected_html_output','{0}.txt'.format(test_file))

    te = TextExtractor(openHtmlFileAsString(html_file))
    expected_output = openTxtFileAsString(expected_output_file)

    self.assertEqual(str(te),expected_output)

  def test4(self):
    test_file = 'example4'
    print(" Testing {0}.html".format(test_file))
    
    html_file = os.path.join('Examples','html_files','{0}.html'.format(test_file))
    expected_output_file = os.path.join('Examples','expected_html_output','{0}.txt'.format(test_file))

    te = TextExtractor(openHtmlFileAsString(html_file))
    expected_output = openTxtFileAsString(expected_output_file)

    self.assertEqual(str(te),expected_output)

  def test5(self):
    test_file = 'example5'
    print(" Testing {0}.html".format(test_file))
    
    html_file = os.path.join('Examples','html_files','{0}.html'.format(test_file))
    expected_output_file = os.path.join('Examples','expected_html_output','{0}.txt'.format(test_file))

    te = TextExtractor(openHtmlFileAsString(html_file))
    expected_output = openTxtFileAsString(expected_output_file)

    self.assertEqual(str(te),expected_output)

  def test6(self):
    test_file = 'example6'
    print(" Testing {0}.html".format(test_file))
    
    html_file = os.path.join('Examples','html_files','{0}.html'.format(test_file))
    expected_output_file = os.path.join('Examples','expected_html_output','{0}.txt'.format(test_file))

    te = TextExtractor(openHtmlFileAsString(html_file))
    expected_output = openTxtFileAsString(expected_output_file)

    self.assertEqual(str(te),expected_output)

  def test7(self):
    test_file = 'example7'
    print(" Testing {0}.html".format(test_file))
    
    html_file = os.path.join('Examples','html_files','{0}.html'.format(test_file))
    expected_output_file = os.path.join('Examples','expected_html_output','{0}.txt'.format(test_file))

    te = TextExtractor(openHtmlFileAsString(html_file))
    expected_output = openTxtFileAsString(expected_output_file)

    self.assertEqual(str(te),expected_output)

  def test8(self):
    test_file = 'example8'
    print(" Testing {0}.html".format(test_file))
    
    html_file = os.path.join('Examples','html_files','{0}.html'.format(test_file))
    expected_output_file = os.path.join('Examples','expected_html_output','{0}.txt'.format(test_file))

    te = TextExtractor(openHtmlFileAsString(html_file))
    expected_output = openTxtFileAsString(expected_output_file)

    self.assertEqual(str(te),expected_output)

  def test9(self):
    test_file = 'example9'
    print(" Testing {0}.html".format(test_file))
    
    html_file = os.path.join('Examples','html_files','{0}.html'.format(test_file))
    expected_output_file = os.path.join('Examples','expected_html_output','{0}.txt'.format(test_file))

    te = TextExtractor(openHtmlFileAsString(html_file))
    expected_output = openTxtFileAsString(expected_output_file)

    self.assertEqual(str(te),expected_output)

################################################
#
# NGRAM TESTS
#
################################################


class NGramTests(unittest.TestCase):
  
  def test1(self):
    print(" BEGINNING NGRAM TESTS")
    test_file = 'example1'
    print(" Testing {0}.txt".format(test_file))

    txt_file = os.path.join('Examples','txt_files','{0}.txt'.format(test_file))
    expected_output_file = os.path.join('Examples','expected_ngram_output','{0}.json'.format(test_file))

    data = ngrams.generate_ngrams(openTxtFileAsList(txt_file),5)
    expected_output = openJsonFile(expected_output_file)

    self.assertDictEqual(data,expected_output)

  def test2(self):
    test_file = 'example2'
    print(" Testing {0}.txt".format(test_file))

    txt_file = os.path.join('Examples','txt_files','{0}.txt'.format(test_file))
    expected_output_file = os.path.join('Examples','expected_ngram_output','{0}.json'.format(test_file))

    data = ngrams.generate_ngrams(openTxtFileAsList(txt_file),5)
    expected_output = openJsonFile(expected_output_file)

    self.assertDictEqual(data,expected_output)

  def test3(self):
    test_file = 'example3'
    print(" Testing {0}.txt".format(test_file))

    txt_file = os.path.join('Examples','txt_files','{0}.txt'.format(test_file))
    expected_output_file = os.path.join('Examples','expected_ngram_output','{0}.json'.format(test_file))

    data = ngrams.generate_ngrams(openTxtFileAsList(txt_file),5)
    expected_output = openJsonFile(expected_output_file)

    self.assertDictEqual(data,expected_output)
  
  def test4(self):
    test_file = 'example4'
    print(" Testing {0}.txt".format(test_file))

    txt_file = os.path.join('Examples','txt_files','{0}.txt'.format(test_file))
    expected_output_file = os.path.join('Examples','expected_ngram_output','{0}.json'.format(test_file))

    data = ngrams.generate_ngrams(openTxtFileAsList(txt_file),5)
    expected_output = openJsonFile(expected_output_file)

    self.assertDictEqual(data,expected_output)
  
  def test5(self):
    test_file = 'example5'
    print(" Testing {0}.txt".format(test_file))

    txt_file = os.path.join('Examples','txt_files','{0}.txt'.format(test_file))
    expected_output_file = os.path.join('Examples','expected_ngram_output','{0}.json'.format(test_file))

    data = ngrams.generate_ngrams(openTxtFileAsList(txt_file),5)
    expected_output = openJsonFile(expected_output_file)

    self.assertDictEqual(data,expected_output)

  def test6(self):
    test_file = 'example6'
    print(" Testing {0}.txt".format(test_file))

    txt_file = os.path.join('Examples','txt_files','{0}.txt'.format(test_file))
    expected_output_file = os.path.join('Examples','expected_ngram_output','{0}.json'.format(test_file))

    data = ngrams.generate_ngrams(openTxtFileAsList(txt_file),5)
    expected_output = openJsonFile(expected_output_file)

    self.assertDictEqual(data,expected_output)

################################################
#
# TEXT EXTRACTOR TESTS
#
################################################
class EndToEnd(unittest.TestCase):
  
  def test1(self):
    test_file = 'example1'
    print(" BEGINNING END TO END TESTS")
    print(" Testing {0}.html".format(test_file))

    html_file = os.path.join('Examples','html_files','{0}.html'.format(test_file))
    expected_output_file = os.path.join('Examples','expected_e2e_test_output','{0}.json'.format(test_file))
    expected_output = openJsonFile(expected_output_file)

    te = TextExtractor(openHtmlFileAsString(html_file))
    data = ngrams.generate_ngrams(te.getListOfWords(),5)

    self.assertDictEqual(data,expected_output)
  
  def test2(self):
    test_file = 'example2'
    print(" Testing {0}.html".format(test_file))

    html_file = os.path.join('Examples','html_files','{0}.html'.format(test_file))
    expected_output_file = os.path.join('Examples','expected_e2e_test_output','{0}.json'.format(test_file))
    expected_output = openJsonFile(expected_output_file)

    te = TextExtractor(openHtmlFileAsString(html_file))
    data = ngrams.generate_ngrams(te.getListOfWords(),5)

    self.assertDictEqual(data,expected_output)
  def test3(self):
    test_file = 'example3'
    print(" Testing {0}.html".format(test_file))

    html_file = os.path.join('Examples','html_files','{0}.html'.format(test_file))
    expected_output_file = os.path.join('Examples','expected_e2e_test_output','{0}.json'.format(test_file))
    expected_output = openJsonFile(expected_output_file)

    te = TextExtractor(openHtmlFileAsString(html_file))
    data = ngrams.generate_ngrams(te.getListOfWords(),5)

    self.assertDictEqual(data,expected_output)
  def test4(self):
    test_file = 'example4'
    print(" Testing {0}.html".format(test_file))

    html_file = os.path.join('Examples','html_files','{0}.html'.format(test_file))
    expected_output_file = os.path.join('Examples','expected_e2e_test_output','{0}.json'.format(test_file))
    expected_output = openJsonFile(expected_output_file)

    te = TextExtractor(openHtmlFileAsString(html_file))
    data = ngrams.generate_ngrams(te.getListOfWords(),5)

    self.assertDictEqual(data,expected_output)
  
  def test5(self):
    test_file = 'example5'
    print(" Testing {0}.html".format(test_file))

    html_file = os.path.join('Examples','html_files','{0}.html'.format(test_file))
    expected_output_file = os.path.join('Examples','expected_e2e_test_output','{0}.json'.format(test_file))
    expected_output = openJsonFile(expected_output_file)

    te = TextExtractor(openHtmlFileAsString(html_file))
    data = ngrams.generate_ngrams(te.getListOfWords(),5)

    self.assertDictEqual(data,expected_output)

  def test6(self):
    test_file = 'example6'
    print(" Testing {0}.html".format(test_file))

    html_file = os.path.join('Examples','html_files','{0}.html'.format(test_file))
    expected_output_file = os.path.join('Examples','expected_e2e_test_output','{0}.json'.format(test_file))
    expected_output = openJsonFile(expected_output_file)

    te = TextExtractor(openHtmlFileAsString(html_file))
    data = ngrams.generate_ngrams(te.getListOfWords(),5)

    self.assertDictEqual(data,expected_output)

  def test7(self):
    test_file = 'example7'
    print(" Testing {0}.html".format(test_file))

    html_file = os.path.join('Examples','html_files','{0}.html'.format(test_file))
    expected_output_file = os.path.join('Examples','expected_e2e_test_output','{0}.json'.format(test_file))
    expected_output = openJsonFile(expected_output_file)

    te = TextExtractor(openHtmlFileAsString(html_file))
    data = ngrams.generate_ngrams(te.getListOfWords(),5)

    self.assertDictEqual(data,expected_output)


'''
Utility to generate all expected output files.
'''
def generate_expected_output():

  if not os.path.exists('Examples'):
    print("ERROR: please invoke this script one level below the 'Examples' directory")
    sys.exit(1)

  if not os.path.exists(os.path.join('Examples','expected_html_output')):
    os.mkdir(os.path.join('Examples','expected_html_output'))


  if not os.path.exists(os.path.join('Examples','expected_ngram_output')):
    os.mkdir(os.path.join('Examples','expected_ngram_output'))


  if not os.path.exists(os.path.join('Examples', 'expected_e2e_test_output')):
    os.mkdir(os.path.join('Examples', 'expected_e2e_test_output'))

  #TEXT EXTRACTION TESTS
  #for all of the html files
  for filename in os.listdir(os.path.join('Examples', 'html_files')):
    file_path = os.path.join('Examples', 'html_files', filename)
    #grab the contents
    with open(file_path, 'r') as infile:
      input_string = infile.read()
    #extract them
    te = TextExtractor(input_string)
    
    #the output file name will be the input file name, but .txt instead of .html.
    outfile_name = "{0}.txt".format(filename.split('.')[0])
    #the output file goes to the expected_html output directory.
    outfile_name = os.path.join('Examples','expected_html_output', outfile_name)
    #dump the results into the output file.
    with open(outfile_name, 'w') as outfile:
      outfile.write(str(te))
      print("Wrote {0}".format(outfile_name))

  #NGRAM TESTS
  #for every text input file.
  for filename in os.listdir(os.path.join('Examples', 'txt_files')):
    file_path = os.path.join('Examples', 'txt_files', filename)
    #grab its contents.
    with open(file_path, 'r') as infile:
      input_string = infile.read().split()
    #Feed them into the ngram generator. We test 5 grams, because that's what's in the system spec.
    data = ngrams.generate_ngrams(input_string, 5)
    #output file name is the input file name .json
    outfile_name = "{0}.json".format(filename.split('.')[0])
    #the output file goes in the expected_ngram_output directory
    outfile_name = os.path.join('Examples','expected_ngram_output', outfile_name)
    #dump a json to the output file.
    with open(outfile_name, 'w') as outfile:
      json.dump(data, outfile)
      print("Wrote {0}".format(outfile_name))

  #E2E TESTS
  #for every html file
  for filename in os.listdir(os.path.join('Examples', 'html_files')):
    file_path = os.path.join('Examples', 'html_files', filename)
    #grab the contents
    with open(file_path, 'r') as infile:
      input_string = infile.read()
    #extract them
    te = TextExtractor(input_string)
    #ngram them
    data = ngrams.generate_ngrams(te.getListOfWords(), 5)
    #the output file name will be the input file name, but .txt instead of .html.
    outfile_name = "{0}.json".format(filename.split('.')[0])
    #the output file goes to the expected_html output directory.
    outfile_name = os.path.join('Examples', 'expected_e2e_test_output', outfile_name)
    #dump the results into the output file.
    with open(outfile_name, 'w') as outfile:
      json.dump(data, outfile)
      print("Wrote {0}".format(outfile_name))

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Unit Testing Framework for the Red M Text Transformation Module. To run tests, invoke using python3 -m unittest {0}'.format(os.path.basename(__file__)))
  
  parser.add_argument('--generate', action="store_true", default=False, help="Generate the expected output for testing")
  args = parser.parse_args()

  if args.generate:
    generate_expected_output()
  else:
    print("ERROR: to generate expected output files, please use the --generate option.\nOtherwise, please call this script as follows:\npython3 -m unittest {0}".format(os.path.basename(__file__)))