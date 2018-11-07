const express = require('express');
const path = require('path');
const app = express();
const routes = require(path.join(__dirname, 'routes'));
const bodyParser = require('body-parser');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));

// Serve static files from ../public
app.use(express.static(path.join(__dirname, '..', 'public')));

const port = process.env.PORT || 8080;
app.listen(port, function() {
  console.log('Listening on port', port);
});

app.use('/server', routes);

module.exports = app;
