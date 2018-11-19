const express = require('express');
const router = new express.Router();
const path = require('path');
const api = require(path.join(__dirname, '..', '/api'));

router.get('/query', (req, res) => {
  try {
    api.getDocIds(req.body.query, (docObj) => {
      const docIds = [];
      for (let i = 0; i < docObj.docs; i++) {
        docIds.push(docObj[i].docid);
      }
      try {
        api.getPages(docIds, res.send);
      } catch (error) {
        res.send([]);
      }
    });
  } catch (error) {
    res.send([]);
  }
});

module.exports = router;
