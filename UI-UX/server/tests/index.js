const path = require('path');
const apiTests = require(path.join(__dirname, 'api'));

apiTests.testGetDocIds();
apiTests.testGetPages();
apiTests.testGetDocIdsAndPages();
