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
            preferences = crud.get_users_preferences(user.user_id)
            return render_template('account.html',
                                user=user,
                                preferences=preferences,)
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
        # used crud function to create a user and bring them to their account page
        if over_21 == "True":
            over_21 = True
        if over_21 == ("False"):
            over_21 = False
        user = crud.create_user(first_name, last_name, email, password, over_21, user_zipcode)
        return render_template ('account.html',
                                user=user)
                        # first_name=first_name,
                        # last_name=last_name,
                        # email=email,
                        # password=password,
                        # over_21=over_21,
                        # user_zipcode=user_zipcode)

    return redirect('/create_account')

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
        preferences = crud.get_users_preferences(user.user_id)
        return render_template ('account.html',
                                user=user,
                                preferences=preferences)

    else:
        return redirect('/')

# @app.route('/account')
# def user_account_page_display():
#     """displays the forms for all the account users info"""
#     print(session)
#  # request.args.get("")
#     return render_template('account.html')

##################################################################################################################

@app.route('/search')
def search_page():
    """takes in info about what to search yelp for """

    print(session)
  
    return render_template('search.html')

# @app.route('/search')
# def actual_search():
#     """takes in info about what to search yelp for """
#     print('hello bitches')
#     zipcode = request.args.get('user_zipcode')

#     return render_template('search_results.html',
#                             zipcode=zipcode,)

@app.route('/search_results')
def rando_results():
    """shows the 5 full results from the search"""

    zipcode = request.args.get('user_zipcode')
    categories = request.args.get('categories')
    address = request.args.get('address')
    # morerandos = request.args.get('fiverandos')
 
    businesses = yelp.yelp_api_query(zipcode, categories, address)

  
    first = [businesses['businesses'][0]['name'],
                businesses['businesses'][0]['id'],
                businesses['businesses'][0]['categories'][0]['title'],
                businesses['businesses'][0]['rating'],
                businesses['businesses'][0]['coordinates'],
                businesses['businesses'][0]['price'],
                businesses['businesses'][0]['location']['display_address'],
                businesses['businesses'][0]['display_phone']]
    second = [businesses['businesses'][1]['name'],
                businesses['businesses'][1]['id'],
                businesses['businesses'][1]['categories'][0]['title'],
                businesses['businesses'][1]['rating'],
                businesses['businesses'][1]['coordinates'],
                businesses['businesses'][1]['price'],
                businesses['businesses'][1]['location']['display_address'],
                businesses['businesses'][1]['display_phone']]
    third = [businesses['businesses'][2]['name'],
                businesses['businesses'][2]['id'],
                businesses['businesses'][2]['categories'][0]['title'],
                businesses['businesses'][2]['rating'],
                businesses['businesses'][2]['coordinates'],
                businesses['businesses'][2]['price'],
                businesses['businesses'][2]['location']['display_address'],
                businesses['businesses'][2]['display_phone']]
    fourth = [businesses['businesses'][3]['name'],
                businesses['businesses'][3]['id'],
                businesses['businesses'][3]['categories'][0]['title'],
                businesses['businesses'][3]['rating'],
                businesses['businesses'][3]['coordinates'],
                businesses['businesses'][3]['price'],
                businesses['businesses'][3]['location']['display_address'],
                businesses['businesses'][3]['display_phone']]
    fifth = [businesses['businesses'][4]['name'],
                businesses['businesses'][4]['id'],
                businesses['businesses'][4]['categories'][0]['title'],
                businesses['businesses'][4]['rating'],
                businesses['businesses'][4]['coordinates'],
                businesses['businesses'][4]['price'],
                businesses['businesses'][4]['location']['display_address'],
                businesses['businesses'][4]['display_phone']]
    list = [first, second, third, fourth, fifth] 
    
    singular_choice = random.choice(list)
    print(singular_choice)
    return render_template ('search_results.html',
                            rando = singular_choice,
                            businesses=businesses,
                            list = list)

    # else:
    #     return render_template('search_results_all.html',
    #                             businesses = businesses)


# @app.route('/all_results')
# def search_results():
#     """shows a list of all the results from the search"""

#     zipcode = request.args.get('user_zipcode')
#     categories = request.args.get('categories')
#     address = request.args.get('address')
 
#     businesses = yelp.yelp_api_query(zipcode, categories, address)

#     return render_template('search_results_all.html',
#                             businesses = businesses)

##################################################################################################################

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)