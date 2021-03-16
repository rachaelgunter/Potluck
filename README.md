# POTLUCK

![Potluck Logo](/static/canva/potlucklogo.png)

Have you ever had the problem where you have TOO MANY choices for dinner?<br/>
What if someone made that choice for you?<br/>
Potluck picks a restaurant for you based on your likes, dislikes and other preferences. <br/>
You're almost guaranteed to like our choice!

## Tech Stack

Front End: HTML5, Jinja2, CSS, JavaScript, AJAX, Bootstrap, jQuery<br/>
Back End: Python, Flask, PostgreSQL, SQLAlchemy, bcrypt<br/>
Database: PostgreSQL<br/>
API: Yelp API<br/>

## Setup & Installation

To have this app running on your local computer, please follow the below steps~

Clone repository~

```bash
$ git clone https://github.com/rachaelgunter/Potluck.git
```

Create and activate a virtual environment~

```bash
$ virtualenv env
$ source env/bin/activate
```

Install requirements~

```bash
$ pip3 install -r requirements.txt
```

Yelp Fusion API uses private API Keys to authenticate requests. To authenticate the call to an endpoint, there are only 2 steps~

1. Create an app to obtain your private API Key.
2. Authenticate API calls with the API Key.

To authenticate API calls with the API Key, set the Authorization HTTP header value as ```Bearer API_KEY```
It is preferred to make your API key a secret key so add it to secrets.sh~

```python
echo "export API_KEY = 'your_authorization_key_here'" > secrets.sh
```  

Add the key to your environmental variables (this will need to be done each time you restart your virtual environment):

```
$ source secrets.sh
```

Create a project database:

```
$ createdb potluck
```

Run Model.py to create your database tables and connect to the server.app:

```
$ python3 -i model.py
>>> connect_to_db(server.app)
>>> db.create_all()
```

Run the server.py to your local host:

```
$ python3 server.py


## Usage


## Developer information 

