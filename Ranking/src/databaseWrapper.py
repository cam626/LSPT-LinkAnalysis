import json
import psycopg2
conn = psycopg2.connect(host = "green-z.cs.rpi.edu",
						dbname = "index",
						user = "ranking",
						password = "ranking",
						port = "5432")

dic = {}
def getInfoFromQuery(query):
	'''
	This function selects query data from database provided by the indexing team
	@parameters: 
		query: a string 
	@returns: a diction with all the single ngram 
	'''
	cur = conn.cursor()
	cur.execute("""
	Select *
	FROM index as i
	JOIN documents as d on i.docid = d.id 
	where i.ngram  = """ + "\'" + query + "\'" )	#concatenate the query with " " to convert to it to type string
	dic = {}
	for row in cur.fetchall():
		docid = str(row[1])
		if not docid in dic:
			dic[docid] = {
				'pagerank': row[9],
				'date_crawled': row[15],#Implement later no data
				'date_update': row[16],
				'in_title': row[2],
				'in_description': row[3],
				'freq_headings': row[5],
				'freq_text': row[6]
		}
	return dic
