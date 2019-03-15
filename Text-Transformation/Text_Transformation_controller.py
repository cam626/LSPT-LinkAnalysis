import text_extract
import ngrams
import json

def Text_Transformation_controller(crawling_data,max_n_gram_size):

    te = text_extract.TextExtractor(crawling_data['metadata']['content'])		#Run the text extractor

    output_link_analysis = dict()													#create the dictionary
    output_link_analysis['links'] = te.getLinksInDocument()						    # Get links from html
    
    output_indexing = dict()													#create the dictionary
    output_indexing['metadata'] = te.extractMetadata()						#Get metadata from html
    output_indexing['metadata']['url'] = crawling_data['url']				#get from crawling API
    output_indexing['metadata']['timestamp'] = crawling_data['metadata']['timestamp'], 	#get from crawling API
    
    list_of_words = te.getListOfWords() 
    n_grams = ngrams.generate_ngrams(list_of_words,max_n_gram_size)
    titles = ngrams.generate_ngrams(te.getTitleListOfWords(),max_n_gram_size)
    headers = ngrams.generate_ngrams(te.getHeaderListOfWords(),max_n_gram_size)
    links = te.getLinksInDocument()

    output_indexing['ngrams'] = {
      'all' : n_grams,
      'headers' : headers, #we need to parse these
      'title' : titles  #we need to parse these.
    }
    output_indexing["text"] = list_of_words
    
    #This line will print the results in output
    print(json.dumps(output_indexing,indent=4))
	
    return (output_indexing, output_link_analysis)

if __name__== "__main__":
    Text_Transformation_controller({'url' : 'www.example.com', 'timestamp' : "2018-11-15T16:25:56+00:00"},5,1)





# The indexing API as agreed upon by slack.
# {
#   "metadata" : {
#     "charset" : "UTF-8",
#     "title" : "TextTransformation",
#     "url" : "indigoO.cs.rpi.edu",
#     "timestamp" : "2018-11-15T16:25:56+00:00",
#     "keywords" : [],
#     "description" : [],
#     "docid" : -1
#   },
#   "ngrams" : {
#     "all" : {
#       "1grams" : {
#         "TextTransformation" : 1,
#         "hello" : 1,
#         "world" : 1,
#         "the" : 1,
#         "end" : 1
#       },
#       "2grams" : {
#         "..." : "etc"
#       }
#     },
#     "headers" :
#     {
#       "1grams" : {
#       "hello" : 1,
#       "world" : 1
#       },
#       "2grams" : {
#         "..." : "etc"
#       }
#     },
#     "title" : {
#       "1grams" : {
#         "TextTransformation" : 1
#       },
#       "2grams" : {
#         "..." : "etc"
#       }
#     }
#   }
# }