from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()

class User(db.Model):
    """model for users"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False,)
    last_name = db.Column(db.String(50), nullable=False,)
    email = db.Column(db.String(50), nullable=False,)
    password = db.Column(db.String(20), nullable=False,)
    over_21 = db.Column(db.Boolean, nullable=False, 
                        unique=False, default=True,)
    user_zipcode = db.Column(db.String(5), nullable=False,)

    def __repr__(self):
        return f'<User user_id = {self.user_id} email = {self.email}>'


class PersonalityTrait(db.Model):
    """model for personality traits"""

    __tablename__ = "personality_traits"

    trait_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True,)
    trait_name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<PersonalityTrait trait_id = {self.trait_id} trait_name = {self.trait_name}>'


class UserPersonalityTrait(db.Model):
    """model for the users personality trait"""

    __tablename__ = "user_personality_traits"

    user_trait_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True,)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),)
    trait_id = db.Column(db.Integer, db.ForeignKey('personality_traits.trait_id'),)

    user = db.relationship('User', backref = 'user_personality_traits')
    trait = db.relationship('PersonalityTrait', backref = 'user_personality_traits')

    def __repr__(self):
        return f'<UserPersonalityTrait user_trait_id = {self.user_trait_id} \
                        user_id = {self.user_id} trait_id = {self.trait_id}>'


class Preference(db.Model):
    """model for preferences"""

    __tablename__ = "preferences"

    preference_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True,)
    preference_name = db.Column(db.String, nullable=False,)

    def __repr__(self):
        return f'<Preference preference_id = {self.preference_id} preference_name = {self.preference_name}>'


class UserPreference(db.Model):
    """model for users preferences"""

    __tablename__ = "user_preference"

    user_preference_id = db.Column(db.Integer,
                                primary_key=True,
                                autoincrement=True,)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),)
    preference_id = db.Column(db.Integer, db.ForeignKey('preferences.preference_id'),)
    
    user = db.relationship('User', backref = 'user_preference')
    preference = db.relationship('Preference', backref = 'user_preference')

    def __repr__(self):
        return f'<UserPreference user_preference_id = {self.user_preference_id} user_id = {self.user_id} preference_id = {self.preference_id}>'


class UserFavoriteRestaurant(db.Model):
    """model for users favorite restaurants"""

    __tablename__ = "user_favorite_restaurants"

    favorite_restaurant_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True,)
    restaurant_id = db.Column(db.String, nullable=False,)
    restaurant_info = db.Column(JSON, nullable=False, default=dict)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),)

    users = db.relationship('User', backref = 'user_favorite_restaurants')

    def __repr__(self):
        return f'<UserFavoriteRestaurant favorite_restaurant_id = {self.favorite_restaurant_id} restaurant_id = {self.restaurant_id} user_id = {self.user_id}>'


def connect_to_db(flask_app, db_uri='postgresql:///project', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    # flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')



if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)