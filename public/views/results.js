/** Gets query from page URL
 * @return {String} a string containing the query
 */
function getQuery() {
  const url = window.location.href;
  return url.slice(url.indexOf('?query=') + 7);
}

const Http = new XMLHttpRequest();
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
        i + '"><h2>' + pages[i].title +
        '</h2><h4><a href=' + pages[i].url +
        '/>'+ pages[i].url +
        '</h4><p>' + pages[i].snippet + '</p></li>');
    }
  }
};

$('document').ready(function() {
  $('#searchbar').val(getQuery());
});
