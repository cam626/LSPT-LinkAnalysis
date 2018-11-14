

function startSearch() {
  const search = document.getElementById("searchbar");
  const query = search.value;
  console.log(query);
  if (query.length==0){
    console.log("Empty query");
  }
  else{
    console.log("Query: "+query);
    window.location = "./results.html";
  }
}
