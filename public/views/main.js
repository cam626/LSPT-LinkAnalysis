/** Append keypress event to the input box */
$('document').ready(function() {
  const input = document.getElementById('searchbar');
  input.addEventListener('keyup', function(event) {
    // Cancel the default action, if needed
    event.preventDefault();
    // If "Enter" key is pressed
    if (event.keyCode === 13) {
      document.getElementById('go-button').click();
    }
  });
});

/** Validate the search query and pass the query to the result page */
function startSearch() {
  const search = document.getElementById('searchbar');
  const query = search.value;
  console.log(query);
  if (query.length==0) {
    console.log('Empty query');
  } else {
    console.log('Query: '+query);
    const url = '/results.html?query='+query;
    window.location = url;
  }
}


/* exported startSearch */
