from flask import Flask, render_template, request, flash, redirect, session

import os
import requests
import crud
from model import connect_to_db
import yelp
import random
from jinja2 import StrictUndefined

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

    # if user in database user crud to get user by email
    #     say that the user already exists and to log in
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
        
        
        # return render_template ('account.html',
        #                         user=user)
        #                 # first_name=first_name,
                        # last_name=last_name,
                        # email=email,
                        # password=password,
                        # over_21=over_21,
                        # user_zipcode=user_zipcode)

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
    # print(drink_prence)
    print(user) 
    preferences = crud.get_all_users_preferences(user.user_id)
    print(preferences)
    
    return render_template('account.html',
                            user=user,
                            preferences=preferences)

##################################################################################################################

@app.route('/account', methods=['GET', 'POST'])
def user_account_page():
    """lists info about the users account
        including preferences and fav restaurants"""
    print(session)
    # session['email'] = email
    print(session)
    # print(user)

    if 'email' in session:
        user = crud.get_user_by_email(session['email'])
        preferences = crud.get_all_users_preferences(user.user_id)
        print(preferences)
        return render_template ('account.html',
                                user=user,
                                preferences=preferences)

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

    print(businesses)

    first = [businesses['businesses'][0]['name'],
                businesses['businesses'][0]['id'],
                businesses['businesses'][0]['categories'][0]['title'],
                businesses['businesses'][0]['rating'],
                businesses['businesses'][0]['coordinates'],
                businesses['businesses'][0]['price'],
                businesses['businesses'][0]['location']['display_address'],
                businesses['businesses'][0]['display_phone'],
                businesses['businesses'][0]['transactions']]
    second = [businesses['businesses'][1]['name'],
                businesses['businesses'][1]['id'],
                businesses['businesses'][1]['categories'][0]['title'],
                businesses['businesses'][1]['rating'],
                businesses['businesses'][1]['coordinates'],
                businesses['businesses'][1]['price'],
                businesses['businesses'][1]['location']['display_address'],
                businesses['businesses'][1]['display_phone'],
                businesses['businesses'][1]['transactions']]
    third = [businesses['businesses'][2]['name'],
                businesses['businesses'][2]['id'],
                businesses['businesses'][2]['categories'][0]['title'],
                businesses['businesses'][2]['rating'],
                businesses['businesses'][2]['coordinates'],
                businesses['businesses'][2]['price'],
                businesses['businesses'][2]['location']['display_address'],
                businesses['businesses'][2]['display_phone'],
                businesses['businesses'][2]['transactions']]
    fourth = [businesses['businesses'][3]['name'],
                businesses['businesses'][3]['id'],
                businesses['businesses'][3]['categories'][0]['title'],
                businesses['businesses'][3]['rating'],
                businesses['businesses'][3]['coordinates'],
                businesses['businesses'][3]['price'],
                businesses['businesses'][3]['location']['display_address'],
                businesses['businesses'][3]['display_phone'],
                businesses['businesses'][3]['transactions']]
    fifth = [businesses['businesses'][4]['name'],
                businesses['businesses'][4]['id'],
                businesses['businesses'][4]['categories'][0]['title'],
                businesses['businesses'][4]['rating'],
                businesses['businesses'][4]['coordinates'],
                businesses['businesses'][4]['price'],
                businesses['businesses'][4]['location']['display_address'],
                businesses['businesses'][4]['display_phone'],
                businesses['businesses'][4]['transactions']]
    list = [first, second, third, fourth, fifth] 
    
    singular_choice = random.choice(list)
    print(singular_choice)
    if businesses:

        return render_template ('search_results.html',
                                rando = singular_choice,
                                businesses=businesses,
                                list = list)

    else:
        flash('Make some selections first!')
        return render_template('search.html')

##################################################################################################################

@app.route('/logout')
# @login_required
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

@app.route('/favorite')
def add_to_favorites():
    """adds a restaurant to your favorites"""

    restaurant = request.args.get('rando')

    if session['email']:
        email = session['email']
        restaurant_id = businesses['businesses'][0]['id']
        crud.add_restaurant_to_favorites(email, restaurant_id, restaurant_info)

    
##################################################################################################################

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)