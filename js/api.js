import "../secrets.ssh"

let restaurantsInfo = []

function getRestaurants(){
    fetch('https://api.yelp.com/v3/businesses/search', {
        method: 'GET',
        headers: `Authorization: Bearer ${YELP_KEY}`
    })
    .then(response => response.json())
    .then(data => restaurantsInfo = data)
}



// $.get()

// $.ajax({

// })

// $.ajax({
//     type: "GET",
//     url: "https://api.yelp.com/v3/businesses/search",
//     headers: { "APIkey": SihnwhuZbWvam081fvWdJH7IXCrHKOghLAYWwA8mlHtO1C5iQWjd2ISEPYMqhPR_NjBn2P8tE_a50n0shb_Q7kAODMtXaDDtRYycf1_BiPdqY2oAdDc6zeu2taIdYHYx },
//     success: function(result){
//       result[i].league_name
//     }
//  });

//  $(document).ready(function () {
//     $.ajax({
//         url: "http://xx.xx.xx.xx:xx/api/values",
//         type: "GET",
//         dataType: "json",
//         headers: { "HeaderName": "MYKey" }
//     });
// });