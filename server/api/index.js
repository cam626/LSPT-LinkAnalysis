const http = require('http');
const {Client} = require('pg');

/** Gets the results JSON for a specific query form ranking
 *  @param {String} query - the query the user searched for
 *  @param {requestCallback} callback - called with an Object containing a pages
 *  array
 */
function getDocIds(query, rankingURL, callback) {
  let parsedData;
  http.get(rankingURL + query, (resp) => {
    const status = resp.statusCode;

    if (status != 200) {
      const error = new Error('Request to ranking was unsuccessful\n');
      console.error(error.message);
      resp.resume();
      return callback( {docs: []} );
    }

    let rawData = '';
    resp.on('data', (chunk) => {
      rawData += chunk;
    });
    resp.on('end', () => {
      try {
        parsedData = JSON.parse(rawData);

        return callback( parsedData );
      } catch (e) {
        console.error(e.message);
        return callback( {docs: []} );
      }
    });
  });
}

/** Gets an array of pages JSONs from indexing
 *  @param {Array} docIds - an array of integers
 *  @param {requestCallback} callback - called with an array
                    containing page information
 */
function getPages(docIds, indexingURL, callback) {
  const client = new Client({
    user: 'querying',
    password: 'querying',
    host: indexingURL,
    port: 5432,
    database: 'index',
  });

  const results = [];
  const text = 'SELECT title, url FROM documents WHERE id=';
  client.connect((error) =>{
    if (error) {
      console.error(error.message);
    }
    console.log('connected');
  });

  let expected_len = docIds.length;
  let actual_len = 0;
  for (let idx = 0; idx < docIds.length; idx++) {

    console.log(docIds[idx]);

    client.query(text + docIds[idx], (error, res) => {
      if (error) {
        console.log(error.message);
        expected_len--;
      }
      else{
        console.log(res.rows[0]);
        results.push(res.rows[0]);
        actual_len++;
        if(actual_len == expected_len){
          client.end();
          callback(results);
        }
      }
    });
  }

  if(actual_len == expected_len){
    client.end();
    callback(results);
  }
}

module.exports = {getDocIds, getPages};
