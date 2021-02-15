
function resultsHidingFunction() {
    var x = document.getElementById("randos");
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  }

  function additionalSearchOptions() {
    var x = document.getElementById("search-options");
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  }

$(document).ready( () => {
  $('#more-choices').click((event) => {
    $("#search-options").toggle();
    console.log(event)
  })
})

$('/favorite').click((event)  => {
  
  
})
