from flask import Flask, render_template, request, flash, redirect, session, jsonify

import os
import requests
import crud
from model import connect_to_db
import yelp
import random
from jinja2 import StrictUndefined
import json

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
SESSION_TYPE = 'null'
# Session(app)

##################################################################################################################

@app.route('/')
def homepage():
    """non post method of homepage """

    return render_template ('homepage.html')

@app.route('/login', methods=['POST'])
def log_in():
    """displays homepage and log in"""

    form_email = request.form.get("login_email")
    form_password = request.form.get("login_password")

    user = crud.get_user_by_email(form_email)
    print("*******", user)

    if user:
        if form_password == user.password: 
            flash(f"logging in!")
            print(user)
            session['email'] = form_email
            print(session)
            print(session['email']) 
            preferences = crud.get_all_users_preferences(user.user_id)
            print(preferences)
            if preferences:
                return render_template('account.html',
                                    user=user,
                                    preferences=preferences,)
            else:
                return render_template('account.html',
                                user=user,)                           
        if form_password != user.password:
            flash(f'incorrect password')
            return render_template('homepage.html')
        
    if user == None:
        flash(f"no user with the {form_email} found! try making an account!")
    
    return redirect('/') 

##################################################################################################################

@app.route('/create_account')
def create_account_page():
    """displays the form to create account"""

    return render_template ('create_account.html')

@app.route('/create_account', methods=['POST'])
def create_user():
    """page to create a new account"""

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")
    over_21 = request.form.get("over_21")
    user_zipcode = request.form.get("user_zipcode")

    user = crud.get_user_by_email(email)
    session['email'] = email

    if user:
        flash('this user already exists with this email')

    else:
        if over_21 == "True":
            over_21 = True
        if over_21 == ("False"):
            over_21 = False
        user = crud.create_user(first_name, last_name, email, password, over_21, user_zipcode)
        return render_template('quiz.html',
                                user=user)
        

    return redirect('/create_account')

@app.route('/quiz', methods=['POST'])
def answer_quiz():
    """form to quiz for new users"""

    print(session['email'])
    email = session['email']
    print(email)

    user = crud.get_user_by_email(email)

    veg = request.form.get('veg')
    if veg == "vegan" or veg == "vegatarian" or veg == "seafood":
        veg_prence = crud.create_user_preference_for_user(veg, email)
    else:  
        pass 
    kosher = request.form.get('kosher')
    if kosher == "kosher":
        kosher_prence = crud.create_user_preference_for_user(kosher, email)
    else:  
        pass 
    drink = request.form.get('drink')
    if drink == "drink":
        drink_prence = crud.create_user_preference_for_user(drink, email)
    else:  
        pass 
    wheel_chair_accessibile = request.form.get('wheel-chair-accessible')
    if wheel_chair_accessibile == "wheel_chair_accessible":
        wheel_chair_accessibile_prence = crud.create_user_preference_for_user(wheel_chair_accessibile, email)
    else:  
        pass 
    gender_neutral_restrooms = request.form.get('gender-neutral-restrooms')
    if gender_neutral_restrooms == "gender_neutral_restrooms":
        gender_neutral_restrooms_prence = crud.create_user_preference_for_user(gender_neutral_restrooms, email)
    else:  
        pass 
    open_to_all = request.form.get('open-to-all')
    if open_to_all == "open_to_all":
        open_to_all_prence = crud.create_user_preference_for_user(open_to_all, email)
    else:  
        pass 

    print(user) 
    preferences = crud.get_all_users_preferences(user.user_id)
    print(preferences)
    favorite_restaurants = crud.get_users_favorites_restaurants(user.email)
    print(favorite_restaurants)
    
    return render_template('account.html',
                            user=user,
                            preferences=preferences,
                            favorite_restaurants=favorite_restaurants)

##################################################################################################################

@app.route('/account', methods=['GET', 'POST'])
def user_account_page():
    """lists info about the users account
        including preferences and fav restaurants"""
    
    print(session)

    if 'email' in session:
        user = crud.get_user_by_email(session['email'])
        preferences = crud.get_all_users_preferences(user.user_id)
        print(preferences)
        print("@@@@@@@", session)
        fave_restaurants = crud.get_users_favorites_restaurants(user.email)
        print(fave_restaurants)
        for item in fave_restaurants:
            print(item.restaurant_info)
            # print(json.loads(item.restaurant_info))
        
        return render_template ('account.html',
                                user=user,
                                preferences=preferences,
                                favorite_restaurants=fave_restaurants)

    else:
        return redirect('/')

##################################################################################################################

@app.route('/search')
def search_page():
    """takes in info about what to search yelp for """

    print(session)
  
    return render_template('search.html')

@app.route('/search_results')
def rando_results():
    """shows the 5 full results from the search"""

    zipcode = request.args.get('user_zipcode')
    categories = request.args.get('categories')
    address = request.args.get('address')
    price = request.args.get('price')
    if price == "$":
        price = 1
    if price == "$$":
        price = 2
    print(price)
    
    #more choices
    hot_and_new = request.args.get('hot-and-new')
    if hot_and_new == "True":
        hot_and_new = True
    if hot_and_new == ("False"):
        hot_and_new = False
    if hot_and_new == None:
        hot_and_new = False
    open_now = request.args.get('open-now')
    if open_now == "True":
        open_now = True
    if open_now == ("False"):
        open_now = False
    if open_now == None:
        open_now = False
    reservations = request.args.get('reservations')
    if reservations == "True":
        reservations = True
    if reservations == ("False"):
        reservations = False
    if reservations == None:
        reservations = False

    print(reservations)
    print(hot_and_new)
    print(zipcode)

    businesses = yelp.yelp_api_query(zipcode, 
                                    categories, 
                                    address, 
                                    price,
                                    hot_and_new,
                                    open_now, 
                                    reservations,)

    list =[]
    print("^^^^^^^^^^^^", businesses)
    
    for business in businesses['businesses']:
        list.append({
                    "name": business["name"],
                    "id": business["id"],
                    "categories": business["categories"][0]['title'],
                    "rating": business["rating"],
                    "coordinates": business["coordinates"],
                    "price": business["price"],
                    "address": business["location"]["display_address"],
                    "phone": business["display_phone"],
                    "transactions": business["transactions"],
        
        })

    
    singular_choice = random.choice(list)
    print("@@@@@@@", singular_choice)
    if businesses:

        return render_template ('search_results.html',
                                rando = singular_choice,
                                businesses=businesses,
                                list = list,)

    else:
        flash('Make some selections first!')
        return render_template('search.html')

##################################################################################################################

@app.route('/logout')
def logout():
    """logs out user by clearing session"""
    print(session)
    if session['email']:
        session.pop('email')
        flash('You were logged out.')
        return redirect('/')
    else: 
        pass
##################################################################################################################

@app.route('/favorite', methods=['GET', 'POST'])
def add_to_favorites():
    """adds a restaurant to your favorites"""

    

    business = request.get_json()
    yelp_id = business['id']
    print("UUUUUUU", type(business))
    print(business['name'])
    print(business['id'])

    if session['email']:
        email = session['email']
        fave_rest = crud.add_restaurant_to_favorites(email, yelp_id, business)
        user = crud.get_user_by_email(email)
        preferences = crud.get_all_users_preferences(user.user_id)
        print(fave_rest)
        print(user)

        flash('Added to your favorites!')
        return render_template('account.html',
                                user=user,
                                preferences=preferences
                                )
     
    else:
        return redirect ("/account")

    print("UUUUUUU", business)
    print(business['name'])
    print(business['id'])



    return jsonify('success')

   
##################################################################################################################

@app.route('/favorite_restaurants', methods=['GET', 'POST'])
def display_favorite_restaurants():
    """displays all favorite restaurants infomation"""
    if session['email']:
        user = crud.get_user_by_email(session['email'])
        fave_rest = crud.get_users_favorites_restaurants(user.email)
        print("#######3", fave_rest)

    return render_template('favrestpage.html',
                            user=user,
                            favorite_restaurants=fave_rest)

##################################################################################################################

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)