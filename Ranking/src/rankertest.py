import unittest
import ranker
import datetime
import databaseWrapper


class MyTestCase(unittest.TestCase):
    def test_retrieve_docs(self):
        query = "fish"
        docs = ranker.retrieve_docs(query, 1)
        check = [{'in_description': True, 'create_date': datetime.date(2018, 1, 15), 'in_title': True,
                  'freq_text': 1.0, 'pagerank': 0.87, 'freq_headings': 0.6666, 'docid': '1'},
                 {'in_description': False, 'create_date': datetime.date(2011, 7, 21), 'in_title': False,
                  'freq_text': 0.769, 'pagerank': 1.12, 'freq_headings': 0.0, 'docid': '2'}]
        self.assertEqual(docs, check)

    def test_transform_features(self):

        docs = [{'docid': i} for i in range(3)]
        for i in docs:
                i['pagerank'] = 1.0
                i['create_date'] = (datetime.date(int(1997), int(01), int(12)))
                i['in_title'] = True
                i['in_description'] = True
                i['freq_headings'] = 0.5
                i['freq_text'] = 0.5

        ranker.transform_features(docs)
        check = [{'in_description': True, 'create_date': datetime.date(1997, 1, 12),
                  'in_title': True, 'freq_text': 0.5, 'pagerank': 1.0, 'freq_headings': 0.5,
                'docid': 0, 'feature_values': {'in_description': 1, 'create_date': 0, 'in_title': 1,
                                               'freq_text': 0.5, 'pagerank': 1.0, 'freq_headings': 0.5}},
                 {'in_description': True, 'create_date': datetime.date(1997, 1, 12),
                  'in_title': True, 'freq_text': 0.5, 'pagerank': 1.0, 'freq_headings': 0.5, 'docid': 1,
                  'feature_values': {'in_description': 1, 'create_date': 0, 'in_title': 1, 'freq_text': 0.5,
                                     'pagerank': 1.0, 'freq_headings': 0.5}},
                 {'in_description': True, 'create_date': datetime.date(1997, 1, 12), 'in_title': True,
                  'freq_text': 0.5, 'pagerank': 1.0, 'freq_headings': 0.5, 'docid': 2,
                  'feature_values': {'in_description': 1, 'create_date': 0, 'in_title': 1,
                                     'freq_text': 0.5, 'pagerank': 1.0, 'freq_headings': 0.5}}]

        self.assertEqual(docs, check)

    def test_get_score(self):

        docs = [{'docid': i} for i in range(3)]
        for i in docs:
                i['pagerank'] = 1.0
                i['create_date'] = (datetime.date(int(1997), int(01), int(12)))
                i['in_title'] = True
                i['in_description'] = True
                i['freq_headings'] = 0.5
                i['freq_text'] = 0.5

        ranker.transform_features(docs)
        score = ranker.get_score(docs)
        check = [{'score': 4.0, 'docid': 0}, {'score': 4.0, 'docid': 1}, {'score': 4.0, 'docid': 2}]
        self.assertEqual(score, check)

    def test_parse_query(self):
        query = "this is crazy!\!#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"
        returnString = ranker.parse_query(query)
        check = "this is crazy"

        self.assertEqual(returnString, check)

    def test_generateNgram(self):
        query = "this is crazy"
        returnString = ranker.generateNgram(query, 1)
        check = ["this", "is", "crazy"]

        self.assertEqual(returnString, check)

    def test_generateNgram_none(self):
        returnString = ranker.generateNgram(None, 1)
        check = "empty query"

        self.assertEqual(returnString, check)

    def test_generateNgram_zero(self):
        query = "this is crazy"
        returnString = ranker.generateNgram(query, 0)
        check = []

        self.assertEqual(returnString, check)

    def test_ranking(self):
        query = "fish"
        res = ranker.ranking(query)
        res.pop("response_time")
        check = {'docs': [{'docid': '1', 'score': 4.5366},
          {'docid': '2', 'score': 1.8890000000000002}], 'query': 'fish'}
        self.assertEqual(res, check)

    def test_ranking_nodocs(self):
        query = "ew"
        res = ranker.ranking(query)
        res.pop("response_time")
        check = {'query': 'ew', 'docs': []}
        self.assertEqual(res, check)

    def test_ranking_nodocs_break(self):
        query = "this is fish"
        res = ranker.ranking(query)
        res.pop("response_time")
        check = {'docs': [{'docid': '1', 'score': 4.5366},
          {'docid': '2', 'score': 1.8890000000000002}],
            'query': 'this is fish'}
        self.assertEqual(res, check)

    def test_dbWarappers(self):
        query = "fish"
        dic = databaseWrapper.getInfoFromQuery(query)
        self.assertIsInstance(dic, dict)

