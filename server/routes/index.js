const express = require('express');
const router = new express.Router();
const path = require('path');
const api = require(path.join(__dirname, '..', '/api'));
const rankingUrls = [
  'http://blue-y.cs.rpi.edu:8080/ranking?query=',
  // 'http://blender01.cs.rpi.edu:8080/ranking?query='
];
const indexingUrls = ['green-z.cs.rpi.edu'];

/** Returns a random url from an array or urls
 * @param {Array} arr an array of urls
 * @return {String} the url
*/
function randUrl(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

/** Creates a 120 character long snippet from the description and paragraphs
 * @param {String} description The description if it exists
 * @param {Array} paragraphs An array of paragraphs that come from database
 * @return {String} a 120 character long string ending in ... if it's truncated
 */
function makeSnippet(description, paragraphs) {
  let snippet = '';
  if (description) paragraphs.unshift(description);
  if (paragraphs && paragraphs.length > 0) {
    snippet += paragraphs.join('... ');
  }
  return snippet.length > 120 ? snippet.slice(0, 197) + '...' : snippet;
}

router.get('/query', (req, res) => {
  api.getDocIds(req.query.query, randUrl(rankingUrls), (docObj) => {
    const docIds = [];

    for (let i = 0; i < docObj.docs.length; i++) {
      docIds.push(docObj.docs[i].docid);
    }
    api.getPages(docIds, randUrl(indexingUrls), (pages) => {
      const processed = pages.map((page) => {
        return {
          'title': page.title,
          'url': page.url,
          'snippet': makeSnippet(page.description, page.paragraphs)};
      });

      res.send(processed);
    });
  });
});

module.exports = router;
