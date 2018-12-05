/** Gets query from page URL
 * @return {String} a string containing the query
 */
function getQuery() {
  let url = window.location.href;
  url = url.slice(url.indexOf('?query=') + 7);
  const urlDecoded = decodeURIComponent(url);
  return urlDecoded;
}

const Http = new XMLHttpRequest();
const listItemStyle = 'line-height:normal;margin:auto';
Http.open('GET', '/server/query?query=' + getQuery());
Http.send();
Http.onreadystatechange = () => {
  if (Http.readyState == 4 && Http.status == 200) {
    const pages = JSON.parse(Http.responseText);
    $('#results-num').text(pages.length == 1 ?
      'There is 1 result' :
      'There are ' + pages.length + ' results');
    for (let i = 0; i < pages.length; i++) {
      $('#list').append('<li id="list-el' +
        i + '" style="margin-bottom:20px">' +
        '<h2 style=' + listItemStyle + '><a class="nounderline" href=' +
        pages[i].url + '>' + pages[i].title +
        '</a></h2><h4 style=' + listItemStyle + '><font color="#325b32">' +
        pages[i].url + '</font></h4><p style=' + listItemStyle + '>' +
        pages[i].snippet + '</p></li>');
    }
  }
};

$('document').ready(function() {
  $('#searchbar').val(getQuery());
});


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
