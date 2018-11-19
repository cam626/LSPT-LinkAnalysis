const express = require('express');
const router = new express.Router();
const path = require('path');
const api = require(path.join(__dirname, '..', '/api'));
const rankingUrls = [
  'http://blue-y.cs.rpi.edu:8080/ranking?query=',
  'http://blender01.cs.rpi.edu:8080/ranking?query='];
const indexingUrls = ['green-z.cs.rpi.edu'];

/** Returns a random url from an array or urls
 * @param {Array} arr an array of urls
 * @return {String} the url
*/
function randUrl(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}


router.get('/query', (req, res) => {
  try {
    api.getDocIds(req.body.query, randUrl(rankingUrls), (docObj) => {
      const docIds = [];
      for (let i = 0; i < docObj.docs; i++) {
        docIds.push(docObj[i].docid);
      }
      try {
        api.getPages(docIds, randUrl(indexingUrls), res.send);
      } catch (error) {
        res.send([]);
      }
    });
  } catch (error) {
    res.send([]);
  }
});

module.exports = router;
