from flask import Flask, render_template, request

import os
import requests

app = Flask(__name__)

@app.route('/', methods=['POST'])
def homepage():
    """displays homepage and log in"""

    #if statement to check if you have an account

    email = request.form.get("email")
    password = request.form.get("password")

    return render_template('homepage.html',
                         email=email, password=password)

@app.route('/create_account', methods=['POST'])
def create_user():
    """page to create a new account"""

    #if statement to check if you have an account

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")
    over_21 = request.form.get("over_21")
    user_zipcode = request.form.get("user_zipcode")

    render_template ('create_account.html',
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                    over_21=over_21,
                    user_zipcode=user_zipcode)

@app.route('/account')
def user_account_page():
    """lists info about the users account
        including preferences and fav restaurants"""
    
    # request.args.get("")

    render_template ('account.html')

@app.route('/search')
def search():
    """takes in info about what to search yelp for """

    render_template ('search.html')

@app.route('/search_results')
def rando_results():
    """shows the chosen results from the search"""

    render_template ('search_results.html')



@app.route('/all_results')
def search_results():
    """shows a list of all the results from the search"""