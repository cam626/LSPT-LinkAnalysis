import json
import os
from collections import Counter
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
  for tup in zipped:
    #create a string out of the words of the gram.
    str_tup = " ".join(tup)
    #update the number of occurrences of the gram.
    occurrences[str_tup] = occurrences.get(str_tup, 0) + 1

  return occurrences

'''
Forward facing function. Takes in a list of words and a value n. Produces all ngrams 0-n.
'''
def generate_ngrams(words, n):
  all_grams = dict()
  for i in range(n):
    current_key = '{0}grams'.format(i+1)
    all_grams[current_key] = i_grams = ngram_helper(words, i+1)
  return all_grams


if __name__ == '__main__':
  words = ["this", "is", "a", "sample", "input", "that", "has", "a", "few","duplicates","to","worry","about","this","is","a","input"]
  n_grams = generate_ngrams(words,3)

  print(json.dumps(n_grams, indent=4))