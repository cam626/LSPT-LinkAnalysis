const assert = require('assert');
const path = require('path');

const apis = require(path.join(__dirname, '..', '..', 'api'));
const rankingURL = 'http://blue-y.cs.rpi.edu:8080/ranking?query=';
const indexingURL = 'green-z.cs.rpi.edu';

/** Tests that getDocIds yields documents */
function testGetDocIds() {
  apis.getDocIds('', rankingURL, (resp) => {
    assert(resp.docs);
    assert(resp.docs.length == 0);
  });

  apis.getDocIds('test test', rankingURL, (resp) => {
    assert(resp.docs);
    assert(resp.docs.length == 0);
  });

  apis.getDocIds('fish', rankingURL, (resp) => {
    assert(resp.docs);
    assert(resp.docs.length == 2);
  });
}

/** Tests that getPages yields pages */
function testGetPages() {
  apis.getPages([], indexingURL, (resp) => {
    // console.log(resp);
    assert(resp.length == 0);
  });

  apis.getPages([1, 2], indexingURL, (resp) => {
    // console.log(resp);
    assert(resp.length != 0);
  });

  apis.getPages([3], indexingURL, (resp) => {
    // console.log(resp);
    assert(resp.length == 0);
  });
  apis.getPages([1, 2, 3], indexingURL, (resp) => {
    // console.log(resp);
    assert(resp.length == 2);
  });
  apis.getPages([1, 3, 2], indexingURL, (resp) => {
    // console.log(resp);
    assert(resp.length == 2);
  });
  apis.getPages([3, 1, 2], indexingURL, (resp) => {
    // console.log(resp);
    assert(resp.length == 2);
  });
}

/** Tests that getDocIds returns valid ids **/
function testGetDocIdsAndPages() {
  apis.getDocIds('', rankingURL, (resp) => {
    assert(resp.docs);
    assert(resp.docs.length == 0);

    apis.getPages(resp.docs, indexingURL, (res) => {
      assert(res.length == 0);
    });
  });

  apis.getDocIds('fish', rankingURL, (resp) => {
    assert(resp.docs);
    assert(resp.docs.length > 0);

    const docIds = [];
    for ( let i = 0; i < resp.docs.length; i++) {
      docIds.push(resp.docs[i].docid);
    }

    apis.getPages(docIds, indexingURL, (res) =>{
      assert(res.length >= 2);
    });
  });
}

module.exports = {testGetDocIds, testGetPages, testGetDocIdsAndPages};
