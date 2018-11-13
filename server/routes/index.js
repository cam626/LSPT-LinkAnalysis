const express = require('express');
const router = new express.Router();
const path = require('path');
const api = require(path.join(__dirname, '../api'));

router.get('/query', (req, res, next) => {
  api.getResults(req.body.query, req.body.pagination)
      .then((results) => res.send);
});

module.exports = router;
