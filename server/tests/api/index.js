const assert = require('assert');
const path = require('path');

const apis = require(path.join(__dirname, '..', '..', 'api'));

function testGetDocIds(){
  let failed = false;
  
  /*
  apis.getDocIds("", (resp) => {
      assert(resp.docs);
      assert(resp.docs.length >= 0);
  });
  */

  apis.getDocIds("test", (resp) => {
    assert(resp.docs);
    assert(resp.docs.length >= 0);
    console.log(resp.docs);
  });
}

module.exports = {testGetDocIds};