const http = require('http');
const rankingURL = "http://blender01.cs.rpi.edu:8080/ranking?query=";
const indexingURL = "";

/** Gets the results JSON for a specific query form ranking
 *  @param {String} query - the query the user searched for
 *  @param {requestCallback} callback - called with an Object containing 
                    a pages array 
 */
function getDocIds(query, callback) {
  let parsedData;
  http.get(rankingURL + query, (resp) => {
    const status = resp.statusCode;
    
    if(status != 200){
      let error = new Error("Request to ranking was unsuccessful\n");
      console.error(error.message);
      resp.resume();
      return callback( { docs: [] } );
    }

    let rawData = '';
    resp.on('data', (chunk) => { rawData += chunk; });
    resp.on('end', () => {
      try{
        parsedData = JSON.parse(rawData);

        return callback( parsedData );
      }
      catch(e){
        console.error(e.message);
        return callback( { docs: [] } );
      }
    });
  });
}

/** Gets an array of pages JSONs from indexing
 *  @param {Array} docIds - an array of integers
 *  @param {requestCallback} callback - called with an array 
                    containing page information
 */
function getPages(docIds, callback){
  let results = [];
  for(const key in docIds){
    if(!docIds.hasOwnProperty(key)){
      continue;
    }
    http.get(indexingURL + key, (resp) =>{
      const status = resp;
      if(status != 200){
        let error = new Error("Request to indexing was unsuccessful\n");
        console.error(error.message);
        resp.resume();
        callback( [] );
      }

      let rawData = '';
      resp.on('data', (chunk) => {
        rawData += chunk; 
      });

      resp.on('end', () => {
        try{
          const parsedData = JSON.parse(rawData);
          results.append(rawData);
        }
        catch(e){
          console.error(e.message);
        }
      });

    });
  }

  callback(results);
}

module.exports = {getDocIds, getPages};