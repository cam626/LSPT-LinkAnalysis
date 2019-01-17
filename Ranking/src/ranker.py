import sys
import logging
import time
import datetime
import requests
import ujson as json
from collections import defaultdict
import psycopg2


logger = logging.getLogger()
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)


def retrieve_docs(query, n=10):
    '''
    Retrieve documents from Indexing

    :param str ngram:
    :param int n: number of documents to retrieve
    :return list docs: retrieved documents
    '''
    conn = psycopg2.connect(host = "green-z.cs.rpi.edu",
                            dbname = "index",
                            user = "ranking",
                            password = "ranking",
                            port = "5432")

    cur = conn.cursor()
    cur.execute("""
    Select *
    FROM index as i
    JOIN documents as d on i.docid = d.id
    where i.ngram  = """ + "\'" + query + "\'" )
    dic = []
    for row in cur.fetchall():
        dic.append({
            'docid': str(row[1]),
            'pagerank': float(row[9]),
            'create_date': row[16],
            'in_title': row[2],
            'in_description': row[3],
            'freq_headings': float(row[5]),
            'freq_text': float(row[6])
        })

    return dic



def transform_features(docs):
    '''
    Transform features for each document

    :param list docs: documents
    '''

    for i in docs:
        # Init
        i['feature_values'] = {}

        # PageRank
        i['feature_values']['pagerank'] = i['pagerank']

        # Freq headings
        i['feature_values']['freq_headings'] = i['freq_headings']

        # Freq text
        i['feature_values']['freq_text'] = i['freq_text']

        # In title
        if i['in_title']:
            i['feature_values']['in_title'] = 1
        else:
            i['feature_values']['in_title'] = 0

        # In description
        if i['in_description']:
            i['feature_values']['in_description'] = 1
        else:
            i['feature_values']['in_description'] = 0

        # Create date
        # cd = i['features']['create_date'].split('-')
        # create_date = datetime.date(int(cd[0]), int(cd[1]), int(cd[2]))
        create_date = i['create_date']
        now = datetime.datetime.now()
        today_date = datetime.date(now.year, now.month, now.day)
        diff = today_date - create_date
        i['feature_values']['create_date'] = 1 / diff.days


def get_score(docs):
    '''
    Compute final score for each document

    :param list docs: documents
    :return list res: list of docid with score
    '''

    scores = defaultdict(float)
    for i in docs:
        s = sum([i['feature_values'][x] for x in i['feature_values']])
        scores[i['docid']] += float(s)
    res = []
    for i, s in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        res.append({'docid': i, 'score': s})
    return res


def parse_query(query):
    '''
    Parse query, remove punctuations and stop words

    :param str query:
    :return str res: parsed query
    '''

    #removes all the punctuations
    exclude = set('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')
    res = ''.join(ch for ch in query if ch not in exclude)
    STOP_WORDS = ['a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for',
                  'from', 'has', 'he', 'i', 'in', 'is', 'it', 'its', 'of',
                  'on', 'that', 'the', 'their', 'we', 'to', 'was', 'were',
                  'with', 'you', 'your', 'yours', 'our', 'ours', 'theirs',
                  'her', 'hers', 'his', 'him', 'mine', 'or', 'but', 'though',
                  'since']
    # res = ' '.join([i for i in res.split() if i not in STOP_WORDS])
    return res


def generateNgram(query, n):
    '''
    The following function reads the query of type string and generate n-grams

    @parameter: query(string): a string query to be read n(int) : an integer
                               that represents the ngrams the user wants to
                               generate.
    @returns: a list "doc" that contains the ngrams of n length or returns
              nothing if n is greater than the number of words in the query
    '''
    doc = []
    if not query:
        return "empty query"
    if n <= 0:
        return []
    wordArray = query.split()
    length = len(wordArray)
    for start in range(len(wordArray)):
            #this handles the case when end index is out of bound
            if start > length - n:
                    break
            ngram_list = wordArray[start:start + n]
            #concatenate the string to ngrams
            ngram = ' '.join(ngram_list)
            doc.append(ngram)
    return doc


def ranking(query, test=False):
    '''
    Main function

    :param str query:
    :return dict res: customized output
    '''

    start_time = time.time()

    query = query.lower()
    parsed_query = parse_query(query)
    docs = retrieve_docs(parsed_query)
    if not docs:
        for n in [5, 4, 3, 2, 1]:
            for i in generateNgram(query, n):
                docs += retrieve_docs(i)
            if docs:
                break

    transform_features(docs)
    scores = get_score(docs)

    response_time = time.time() - start_time

    res = {
        'query': query,
        'docs': scores,
        'response_time': response_time
    }
    if test:
        res['test'] = docs
    return res


if __name__ == '__main__':
    import pprint
    pprint.pprint(ranking('fish'))
    pprint.pprint(ranking('fish', True))
