# LSPT-LinkAnalysis
Link Analysis part for search engine project in LSPT course

## Usage

#### To compile
make -f graph_test.mk
#### To run the program
Open four terminals. The program runs in the first terminal by using 
./listener.out

The second terminal simulates the text transformation, which sends web links to link analysis program in Json files. 
curl -XPUT -H’Content-Type: application/json’ LINK_ANALYSIS_ADDRESS:9080/family_person?pretty -d@TEST_JSON_FILE.json

The third terminal simulates the function that link analysis program sends the web link to crawling team. 
nc -l  CRAWLING_ADDRESS 9877

The fourth terminal simulates the function that link analysis program sends the page rank to the index team. 
nc -l INDEXING_ADDRESS 9876

## Testing

#### Run the program
./listener.out
nc -l  localhost 9877
nc -l  localhost 9876

#### Unit test
curl -XPUT -H’Content-Type: application/json’ localhost:9080/family_person?pretty -d@tt.json

Then the correspoding web links and page ranks will be shown in the third and fourth terminal.

#### Pressure test

create the tesing Json files:
cd Create_test_json
python generate_test_json.py 

use Curl to parse these Json files simultaneously:
curl -XPUT -H’Content-Type: application/json’ LINK_ANALYSIS_ADDRESS:9080/family_person?pretty -d@TEST_JSON_FILE.json

