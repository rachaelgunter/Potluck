
function resultsHidingFunction() {
    var x = document.getElementById("randos");
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  }


// this is for the more options before the search //

function additionalSearchOptions() {
  var x = document.getElementById("#search-options");
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

// function for adding a favorite user restaurant //

function favoriteRestaurant(evt) {
  evt.preventDefault();

  let url = "/favorite";
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

// view the users favorite restaurants on a page //

function viewFaves() {
  evt.preventDefault();

  let url = "/account"
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

// make a random choice from the favorite restaurants //

function randomChoiceFaveRest() {

  let url = "/random_favorite";
  $.get(url, (resp) => { 
    console.log(resp);
  $("#fave-rest-random-choice").html(resp.restaurant_info['name'])
  $("#fave-rest-random-choice").append(resp.restaurant_info.categories)
  $("#fave-rest-random-choice").append(resp.restaurant_info.phone)
  $("#fave-rest-random-choice").append(resp.restaurant_info.rating)
  $("#fave-rest-random-choice").append(resp.restaurant_info.address)
  $("#fave-rest-random-choice").append(resp.restaurant_info.transactions)
  });
}


//event listeners 

$('#favorite-restaurant').on('click', favoriteRestaurant);

$('#favorite-restaurant-2').on('click', favoriteRestaurant);

$('#favorite-restaurants').on('click', viewFaves);

// $('#random-favorite').on('click', randomChoiceFaveRest);


