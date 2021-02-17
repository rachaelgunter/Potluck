from model import User, Preference, PersonalityTrait, UserPersonalityTrait, UserPreference, UserFavoriteRestaurant, connect_to_db, db

def create_user(first_name, last_name, email, password, over_21, user_zipcode):
    """creates and returns a new user"""

    user = User(first_name=first_name, last_name=last_name, email=email, password=password, over_21=over_21, user_zipcode=user_zipcode)

    db.session.add(user)
    db.session.commit()

    return user

def create_preference(preference_name):
    """creates and returns a preference"""

    preference = Preference(preference_name=preference_name)

    db.session.add(preference)
    db.session.commit()

    return preference

def create_user_preference(user_id, preference_id):
    """creates and returns a user preference"""

    user_prence = UserPreference(user_id=user_id, preference_id=preference_id)

    db.session.add(user_prence)
    db.session.commit()

    return user_prence

def create_trait(trait_name):
    """creates and returns a trait"""

    ptrait = PersonalityTrait(trait_name=trait_name)

    db.session.add(ptrait)
    db.session.commit()

    return ptrait

def create_user_ptrait(user_id, trait_id):
    """creates and returns a user personality trait"""

    user_ptrait = UserPersonalityTrait(user_id=user_id, trait_id=trait_id)

    db.session.add(user_ptrait)
    db.session.commit()

    return user_ptrait

def create_user_fav_restaurant(restaurant_id, user_id, restaurant_info):
    """creates and returns a users favorite restaurant"""

    user_fav_rest = UserFavoriteRestaurant(restaurant_id=restaurant_id, user_id=user_id, restaurant_info=restaurant_info)

    db.session.add(user_fav_rest)
    db.session.commit()

    return user_fav_rest

def get_user_by_email(email):
    """returns user_id from email"""

    user = User.query.filter(User.email==email).first()

    return user

def get_users_preferences(user_id):
    """returns a list of users preferences"""
    
    user_preference = UserPreference.query.filter(User.user_id==user_id).first()
    preferences = Preference.query.filter(user_preference.preference_id==user_preference.preference_id).all()

    return preferences

def log_out():
    """log out session"""

    session.pop('email')

def create_user_preference_for_user(preferencename, email):
    """create a preference and user preference by user email"""
    
    user = get_user_by_email(email=email)
    userpreferences = get_all_users_preferences(user_id=user.user_id)
    list_prefs = []
    for pref in userpreferences:
        list_prefs.append(pref.preference_name)
    print(list_prefs)
    if preferencename not in list_prefs:
        preference = create_preference(preference_name=preferencename)
        user = get_user_by_email(email=email)
        user_prence = create_user_preference(user.user_id, preference.preference_id)
        print("OKOKOK", user_prence)

    # preference_set = []
    # prefs = get_all_users_preferences(user_id=user.user_id)
    # print(preference_set)
    # for pref in prefs:
    #    preference_set.append(pref)
    
    # preference_set = set(preference_set)


        return user_prence

def get_all_users_preferences(user_id):
    """returns a list of all users preferences (user_preference_id)"""

    user_prefs = []
    preferences = UserPreference.query.filter_by(user_id=user_id).all()
    for preference in preferences:
        preference_id = preference.preference_id
        temp = Preference.query.get(preference_id)
        user_prefs.append(temp)
    # print(user_prefs)

    return user_prefs


def get_users_preferences(user_id):
    """returns a list of users preferences"""
    
    user_preference = UserPreference.query.filter(User.user_id==user_id).first()
    preferences = Preference.query.filter(user_preference.preference_id==user_preference.preference_id).all()

    return preferences

def add_restaurant_to_favorites(email, restaurant_id, restaurant_info):
    """add a restaurant to a list of users favorites"""

    user = get_user_by_email(email=email)
    restaurant = UserFavoriteRestaurant.query.filter(UserFavoriteRestaurant.restaurant_id==restaurant_id).all()
    if not restaurant:
        fav_restaurant = create_user_fav_restaurant(restaurant_id, user.user_id, restaurant_info)
        print("!(!(!(!(!(!(!(", fav_restaurant.restaurant_id)

    return fav_restaurant

def get_users_favorites_restaurants(email):

    """get favorites restaurnats by user"""

    user = get_user_by_email(email=email)
    list_faves = UserFavoriteRestaurant.query.filter_by(user_id=user.user_id).all()

    return list_faves


if __name__ == '__main__':
    from server import app
    connect_to_db(app)



