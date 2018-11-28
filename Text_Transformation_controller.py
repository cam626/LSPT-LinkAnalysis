import text_extract
import ngrams

def main():
    path = 'Examples/example1.html'
    te = text_extract.TextExtractor(path)
    n_grams = ngrams.generate_ngrams(te.getListOfWords(),3)

    for gram, count in n_grams.items():
        print("{0}: {1}".format(gram, count))

if __name__== "__main__":
    main()