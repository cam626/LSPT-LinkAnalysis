
//send a request to the router to get the Results
//recieve the results from the router
  //object with all the links inside it


//variables that need to be firgured out
const link1 = {title:"Tile", url:"www.link.com"}
const link2 = {title:"Tile", url:"www.link.com"}
const link3 = {title:"Tile", url:"www.link.com"}
const link4 = {title:"Tile", url:"www.link.com"}
const link5 = {title:"Tile", url:"www.link.com"}
const results = [link1, link2, link3, link4, link5];
const num_results = 10; //so we know how many pages to have
current_page = 1; //so we can check the prev and next buttons

/*function to add the 10 results (less if necessary)
calls another function to display the no results pages
if there are no results*/
function displayResults () {
  newTitle = document.createElement('h2');
  titleText = document.createTextNode(results[0].title);
  newLink = document.createElement('h4');
  linkText = document.createTextNode(results[0].url);
  newTitle.appendChild(titleText);
  newLink.appendChild(linkText);
  list_el = document.createElement('li');
  list_el.appendChild(newTitle);
  list_el.appendChild(newLink);
  document.getElementById("list").appendChild(list_el);

}

//function to return the no results pages
//check if num results == 0
function displayNoResults() {

}

//function to determine if next page button is needed
// (places it if needed)
function displayNextButton() {

}

//function to determine if prev page button is needed
// (places it if needed)
function displayPrevButton() {

}
