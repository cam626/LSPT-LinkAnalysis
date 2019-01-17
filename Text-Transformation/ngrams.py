import json
import os
from collections import Counter
import argparse

with open("Data/stopwords.txt", 'r') as infile:
  stopwords = infile.read().split()

'''
The fully armed and operational n_gram module.
'''


'''
Helper function, constructs all n_grams of size n, returns a counter dict.
'''
def ngram_helper(words, n):
  #create a list of iterators to generate on. (This could be a one liner, but I felt it was more readable this way.)
  iterators = list()
  for i in range(n):
    iterators.append(words[i:])
  #zip together the iterators. The * expand/de-lists/de-references the iterator list.
  zipped = zip(*iterators)

  #now that we have our iterators, we can iterate over them,
  occurrences = dict()
  flag = False
  for tup in zipped:
    #create a string out of the words of the gram.
    for word in tup:
        if word in stopwords:
          flag = True
          break
    if not flag:
      str_tup = " ".join(tup)
      #update the number of occurrences of the gram.
      occurrences[str_tup] = occurrences.get(str_tup, 0) + 1
    flag = False
  return occurrences

'''
Forward facing function. Takes in a list of words and a value n. Produces all ngrams 0-n.
'''
def generate_ngrams(words, n):
  all_grams = dict()
  for i in range(n):
    current_key = '{0}grams'.format(i+1)
    all_grams[current_key] = ngram_helper(words, i+1)
  return all_grams


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  
  parser.add_argument('--string', action="store_true", default=False, help="Pass in a string to turn into ngrams.")
  parser.add_argument('--n', default=5,  help="Pass in an n value for your run (defaults to 5).")
  parser.add_argument('arg1', nargs='+', help="Either the path to an input file OR, if you specify --string, an input string")

  args = parser.parse_args()

  if args.string == True:
    print("An input string")
    inpt = args.arg1
  elif len(args.arg1)> 1:
    print("ERROR: Too many command line arguments. Did you mean to specify --string?")
    sys.exit(1)
  else:
    path = args.arg1[0]
    with open(path, 'r') as myfile:
      inpt = myfile.read().split()


  n_grams = generate_ngrams(inpt,int(args.n))

  print(json.dumps(n_grams, indent=4))