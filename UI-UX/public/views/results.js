/** Gets query from page URL
 * @return {String} a string containing the query
 */
function getQuery() {
  let url = window.location.href;
  const queryIndex = url.indexOf('?query=');
  const pageIndex = url.indexOf('&page=');
  url = url.slice(queryIndex + 7, pageIndex);
  const urlDecoded = decodeURIComponent(url);
  return urlDecoded;
}
/** Get the page number got clicked on
 * @return {int} the page number selected
 */
function getSelectedPageNumber() {
  const url = window.location.href;
  const pageIndex = url.indexOf('&page=');
  const pageNum = parseInt(url.slice(pageIndex + 6));
  return pageNum;
}

const defaultNumResPerPage = 1;
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
    // display results based on the current page number
    const currPageNum = getSelectedPageNumber();
    const totalPageNum = Math.ceil(pages.length / defaultNumResPerPage);
    // only show pagination if there are more than one page
    if (pages.length > defaultNumResPerPage) {
      const currUrl = window.location.href;
      const pageIndex = currUrl.indexOf('&page=');
      const newUrl = currUrl.slice(0, pageIndex);
      for (let i = 1; i <= totalPageNum; i++) {
        const redirectUrl = newUrl + '&page=' + (i);
        if (i == currPageNum) {
          $('#pagination-list').append('<li class="active"><a href="' +
            redirectUrl + '">' + i + '</a></li>');
        } else {
          $('#pagination-list').append('<li><a href="' +
            redirectUrl + '">' + i + '</a></li>');
        }
      }
    }

    for (let i = (currPageNum - 1) * defaultNumResPerPage;
      i < (currPageNum) * defaultNumResPerPage; i++) {
      $('#list').append('<li id="list-el' +
        i + '" style="margin-bottom:20px">' +
        '<h2 style=' + listItemStyle + '><a class="nounderline" href=' +
        pages[i].url + '>' + pages[i].title +
        '</a></h2><h4 style=' + listItemStyle + '><font color="#325b32">' +
        pages[i].url + '</font></h4><p style=' + listItemStyle + '>' +
        pages[i].snippet + '</p></li>');

      if (i == pages.length - 1) {
        return;
      }
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
    const url = '/results.html?query='+query+'&page=1';
    window.location = url;
  }
}


/* exported startSearch */
