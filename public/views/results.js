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
    console.log(pages);
  }
};

document.getElementById("searchbar").placeholder = getQuery();
