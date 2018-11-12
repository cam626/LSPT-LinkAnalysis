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
  all_ngrams = Counter()
  for i in range(n):
    #generate all i_grams
    i_grams = ngram_helper(words, i)
    #append them to the all_grams dict
    all_ngrams.update(i_grams)
  return dict(all_ngrams)


if __name__ == '__main__':
  words = ["this", "is", "a", "sample", "input", "that", "has", "a", "few","duplicates","to","worry","about","this","is","a","input"]
  n_grams = generate_ngrams(words,3)

  for gram, count in n_grams.items():
    print("{0}: {1}".format(gram, count))