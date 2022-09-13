from . import api
from .auth import basic_auth, token_auth
from flask import jsonify, request
from app.models import Suggestion, User


@api.route('/token')
@basic_auth.login_required
def get_token():
    user = basic_auth.current_user() # current_user is the user instance from authentication method
    token = user.get_token() # call get_token method on user
    return jsonify({'token': token, 'token_expiration': user.token_expiration})


# get all of the suggestions and convert the data into a json response
@api.route('/suggestions', methods= ["GET"])
def get_suggestions():

    suggestions = Suggestion.query.all()
    return jsonify([s.to_dict() for s in suggestions]) # list comprehension 
    # to_dict for every suggestion in suggestions 



# get one suggestion and convert the data into a json response
@api.route('/suggestions/<suggestion_id>')
@token_auth.login_required
def get_suggestion(suggestion_id):

    # query either returns a suggestion if it exists or 404 if it does not exist
    suggestion = Suggestion.query.get_or_404(suggestion_id) # the .get method searches by primary key
    return jsonify(suggestion.to_dict())



# create a suggestion with a post request
@api.route('/suggestions', methods=["POST"])
# @token_auth.login_required ## ADD LOGIN REQUIRED TO CREATE SUGGESTIONS AFTER I ADD BASE SUGGESTIONS
def create_suggestion():

    # if request is not a json body
    if not request.is_json: # send back a tuple that's a json reponse with a 400 status code
        return jsonify({'error': 'Your request content-type must be application/json'}), 400

    # get the data from the request body
    data = request.json

    # validate the data
    for field in ['activity', 'category', 'participants', 'price', 'user_id']: ## COME BACK AND REMOVE 'USER_ID'
        if field not in data:

            # if field not in request body, return error
            return jsonify({'error': f'<{field}> must be in request body'}), 400

    # if data validated get fields from data dict
    activity = data.get('activity')
    category = data.get('category')
    participants = data.get('participants')
    price = data.get('price')
    user_id = data.get('user_id') ## REMOVE THIS LINE
    # user = token_auth.current_user() ## UNCOMMENT THIS LINE OUT
    # user_id = user.id ## AND UNCOMMENT THIS LINE

    # create a new instance of suggestion with data
    new_suggestion = Suggestion(activity=activity, category=category, 
        participants=participants, price=price, user_id=user_id)

    return jsonify(new_suggestion.to_dict()), 201



# get one user by id and convert the data into a json response
@api.route('/users/<user_id>')
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())



# create a new user
@api.route('/users', methods=["POST"])
def create_user():
    # if request is not json body
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    
    # if request is json body get the data from the request
    data = request.json

    # make sure data has all the required fields
    for field in ['email', 'username', 'password']:
        if field not in data:
            return jsonify({'error': f'<{field}> must be in request body'}), 400

    # if data validated get fields from data dict
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    # before we add a new user to the database, check to see if there is already 
    # a user with that email or username
    existing_user = User.query.filter((User.email == email) | (User.username == 
        username)).first()
    
    # if there is an existing user return json error
    if existing_user:
        return jsonify({'error': 'User with username and/or email already exists'}), 400

    # create a new instance of user
    new_user = User(email=email, username=username, password=password)
    return jsonify(new_user.to_dict()), 201
