import text_extract
import ngrams
import json

def Text_Transformation_controller(crawling_data,max_n_gram_size,max_threads):
    path = 'Examples/example1.html'

    te = text_extract.TextExtractor(path)
    
    output = dict()
    output['metadata'] = te.extractMetadata()
    output['metadata']['url'] = crawling_data['url']
    output['metadata']['timestamp'] = crawling_data['timestamp'], #get from crawling API
    
    n_grams = ngrams.generate_ngrams(te.getListOfWords(),max_n_gram_size)
    titles = ngrams.generate_ngrams(te.getTitleListOfWords(),max_n_gram_size)
    headers = ngrams.generate_ngrams(te.getHeaderListOfWords(),max_n_gram_size)

    output['ngrams'] = {
      'all' : n_grams,
      'headers' : headers, #we need to parse these
      'title' : titles  #we need to parse these.
    }

    #This line will print the results in output
    print(json.dumps(output,indent=4))

    ###########################################
    # We forward to link analysis here.
    ############################################
    '''
    link_json = {
      'base_url' : url # the url we recieved from the crawling api call.
    }


    '''


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