import os
import json
from random import choice, random, randint

import model
import crud
import server
import psycopg2
import bcrypt
import scrypt

os.system('dropdb project')
os.system('createdb project')

model.connect_to_db(server.app)
model.db.create_all()

# def hashed(password):
#     print("$$$$$$$", password)
#     encrypted_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(10))
#     print('this is encrytped pw' , encrypted_password)
#     return encrypted_password

# def hashed(password, maxtime=0.5, datalength=64):
#     print("$$$$$$$", password)
#     encrypted_password = scrypt.encrypt(os.urandom(datalength), password, maxtime=maxtime)
#     print('this is encrytped pw' , encrypted_password)
#     return encrypted_password

# #seeding traits 
# for n in range(3):
#     trait_name = f'trait {n}'
#     # print(trait_name)
#     ptrait = crud.create_trait(trait_name)

# #seeding preferences 
# for n in range(3):
#     preference_name = f'preference {n}'

#     prence = crud.create_preference(preference_name)

# #seeding users and their traits
# for n in range(1, 21):
#     first_name = f'first-{n}'
#     last_name = f'last-{n}'
#     email = f'user{n}@test.com'
#     password = 'test'
#     password_hashed = crud.hashed(password)
#     over_21 = choice([True, False])
#     user_zipcode = '11220'

#     user = crud.create_user(first_name, last_name, email, password_hashed, over_21, user_zipcode)

# for n in range(3):
#     user_id = randint(1, 21)
#     trait_id = randint(1, 3)

#     user_ptrait = crud.create_user_ptrait(user_id, trait_id)

# for n in range(3):
#     user_id = randint(1, 21)
#     preference_id = randint(1, 3)

#     user_prence = crud.create_user_preference(user_id, preference_id)

# key = ["_M5FVY4hkcuU-ASdVZPfRQ", "isIFCDLE3VIDJcqhVy_klA", "O-zwQQV8AExgdPoJiqjpDg"]

# for n in range(3):
#     restaurant_id = choice(key)
#     user_id = randint(1, 21) 
    
#     fav_restaurant = crud.create_user_fav_restaurant(restaurant_id, user_id)   
    