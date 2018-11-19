const assert = require('assert');
const path = require('path');

const apis = require(path.join(__dirname, '..', '..', 'api'));
const rankingURL = 'http://blender01.cs.rpi.edu:8080/ranking?query=';
const indexingURL = 'green-z.cs.rpi.edu';
/** Tests that getDocIds yeilds documents */

function testGetDocIds() {
  apis.getDocIds('', rankingURL, (resp) => {
    assert(resp.docs);
    assert(resp.docs.length >= 0);
  });
    
  apis.getDocIds('test test', rankingURL, (resp) => {
    assert(resp.docs);
    assert(resp.docs.length >= 0);
  });

  apis.getDocIds('test', rankingURL, (resp) => {
    assert(resp.docs);
    assert(resp.docs.length >= 0);
  });
}


function testGetPages() {
  apis.getPages([], indexingURL, (resp) => {
    console.log(resp);
    assert(resp.length == 0);
  });
  
  apis.getPages([1,2], indexingURL, (resp) => {
    console.log(resp);
    assert(resp.length != 0);
  });

  apis.getPages([3], indexingURL, (resp) => {
    console.log(resp);
    assert(resp.length == 0);
  });
}
module.exports = {testGetDocIds, testGetPages};
