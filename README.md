# LSPT-LinkAnalysis
Link Analysis part for search engine project in LSPT course

## Usage

#### To compile
make -f graph_test.mk
#### To run the program
Open four terminals. The program runs in the first terminal by using 
./listener.out

The second terminal simulates the text transformation, which sends web links to link analysis program in Json files. 
curl -d @TEST_JSON_FILE.json LINK_ANALYSIS_ADDRESS:9080

The third terminal simulates the function that link analysis program sends the web link to crawling team. 
nc -l 127.0.0.1 9877

The fourth terminal simulates the function that link analysis program sends the page rank to the index team. 
nc -l 127.0.0.1 9876

## Testing

#### Run the program
./listener.out
nc -l  localhost 9877
nc -l  localhost 9876

#### Unit test

Simulating Text Transformation. This will start the process of communication with all groups and will therefore test all transactions in a single workflow.
curl -d @tt.json http://localhost:9080
curl -d @tt2.json http://localhost:9080
curl -d @tt3.json http://localhost:9080

The correspoding web links and page ranks will be shown in the third and fourth terminal.

#### Pressure test

create the tesing Json files:
cd Create_test_json
python generate_test_json.py 

use Curl to parse these Json files simultaneously:
curl -d @TEST_JSON_FILE.json LINK_ANALYSIS_ADDRESS:9080

