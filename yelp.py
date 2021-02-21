import requests
import json
from json2html import *
import os

def yelp_api_query(zipcode, categories, *args):
    YELP_KEY = os.environ['YELP_KEY']
    headers = {'Authorization': 'Bearer %s' % YELP_KEY}

    url='https://api.yelp.com/v3/businesses/search'
    params = {'limit': 5, 
            'location': zipcode, 
            # 'categories': "restaurants",
            'categories': categories,}
            # 'address': address,
            # 'price': price,
            # 'hot_and_new': hot_and_new,
            # 'open_now': open_now,
            # 'reservations': reservations
    req=requests.get(url, params=params, headers=headers)

    businesses = json.loads(req.text)

    print(type(businesses))
    if 'error' in businesses:
        return businesses
    else:
        for business in businesses['businesses']:
            if "price" not in business:
                business['price'] = "$*"    
        return businesses
   
    
    # businesses = businesses['businesses']
            
    

# business = {"name": business["name"]
#                     "id": business["id"],
#                     "categories": business["categories"][0]['title'],
#                     "rating": business["rating"],
#                     "coordinates": business["coordinates"],
#                     "price": f'price: $$$$$$$',
#                     "address": business["location"]["display_address"],
#                     "phone": business["display_phone"],
#                     "transactions": business["transactions"],}




# input = businesses 
# print(json.dumps(businesses, indent=4, sort_keys=True))
# print(businesses)

# print(businesses.keys())
# print(businesses['businesses'][0]['name'])

# name = businesses['businesses'][0]['name'] 

# print(name)

# json2html.convert(json = input)

# print(businesses['businesses'][0]['name']) 
# print(businesses['businesses'][0]['id'])
# print(businesses['businesses'][0]['categories'][0]['title'])
# print(businesses['businesses'][0]['rating'])
# print(businesses['businesses'][0]['coordinates'])
# print(businesses['businesses'][0]['price'])
# print(businesses['businesses'][0]['location']['display_address'])
# print(businesses['businesses'][0]['display_phone'])

# return businesses

# businesses['businesses'][0]['name'] = name of restaurant
# businesses['businesses'][0]['id'] = yelp api id 
# businesses['businesses'][0]['categories'][0]['title'] = title 
# businesses['businesses'][0]['rating'] = rating 
# businesses['businesses'][0]['coordinates'] = coordinates 
# businesses['businesses'][0]['price'] = price in dollar signs 
# businesses['businesses'][0]['location']['display_address'] = address
# (businesses['businesses'][0]['display_phone'] = phone 
