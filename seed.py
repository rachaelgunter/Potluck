import os
import json
from random import choice, random, randint

import model
import crud
import server
import psycopg2

os.system('dropdb project')
os.system('createdb project')

model.connect_to_db(server.app)
model.db.create_all()

#seeding traits 
for n in range(3):
    trait_name = f'trait {n}'
    # print(trait_name)
    ptrait = crud.create_trait(trait_name)

#seeding preferences 
for n in range(3):
    preference_name = f'preference {n}'

    prence = crud.create_preference(preference_name)

#seeding users and their traits
for n in range(20):
    first_name = f'first-{n}'
    last_name = f'last-{n}'
    email = f'user{n}@test.com'
    password = 'test'
    over_21 = choice([True, False])
    user_zipcode = '11220'

    user = crud.create_user(first_name, last_name, email, password, over_21, user_zipcode)

for n in range(3):
    user_id = randint(1, 20)
    trait_id = randint(1, 3)

    user_ptrait = crud.create_user_ptrait(user_id, trait_id)

for n in range(3):
    user_id = randint(1, 20)
    preference_id = randint(1, 3)

    user_prence = crud.create_user_preference(user_id, preference_id)

    # for n in range(3):
    #     restaurant_id = 
    #     user_id = random.randint(1, 20) 

    #     fav_restaurant = model.UserFavoriteRestaurant(restaurant_id, user_id)   
     