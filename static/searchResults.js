
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
    if (x.style.display === "anone") {
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

function favoriteRestaurant(evt) {
  evt.preventDefault();

  let url = "/favorite";
  //let url2 = "/account" mehbeh
  // let formData = {"businesses": $("#favorite-restaurant").html()};
  let formData = {
    "name": $("#restaurant-name").html(),
    "id": $("#restaurant-id").html(),
    "categories": $("#restaurant-categories").html(),
    "rating": $("#restaurant-rating").html(),
    "coordinates": $("#restaurant-coordinates").html(),
    "price": $("#restaurant-price").html(),
    "address": $("#restaurant-address").html(),
    "phone": $("#restaurant-phone").html(),
    "transactions": $("#restaurant-transactions").html()
  }
  console.log(url)
  console.log(formData)

  fetch(url, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(formData)
  })
  .then((response) => response.json())
  .then((data) => console.log(data));


}
    
$('#favorite-restaurant').on('click', favoriteRestaurant);

function viewFaves() {
  evt.preventDefault();

  let url = "/favorite_restaurants"
  let formData = {
    "Restaurant": $("#restaurant-name").html()
  }
  console.log(url)
  console.log(formData)

  fetch(url, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(formData)
  })
}