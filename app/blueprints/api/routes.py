from . import api
from .auth import basic_auth, token_auth
from flask import jsonify, request
from app.models import Suggestion, User

############## USER ROUTES ##############

# log the user in and isse then a token and token expiration
@api.route('/token')
@basic_auth.login_required
def get_token():
    user = basic_auth.current_user() # current_user is the user instance from authentication method
    token = user.get_token() # call get_token method on user
    return jsonify({'token': token, 'token_expiration': user.token_expiration})


# get one user by id and convert the data into a json response
@api.route('/users/<user_id>', methods=['GET'])
@token_auth.login_required # the user should be logged in to see other user data
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


# the PUT method replaces whatever exists at the target URL with something else (update)
@api.route('/users/<user_id>', methods=["PUT"]) 
@token_auth.login_required
def update_user(user_id):
    # set a variable as the current_user data
    current_user = token_auth.current_user()
    # if the current_user id does not match the passed in user_id they are not 
    # authorized to update that user
    if current_user.id != int(user_id): # the user_id is originally a string and I had to convert to an integer
        # send 403 error response (forbidden) meaning the user has been authenticated
        # but they do not have access rights to the content
        return jsonify({'error': 'You are not authorized to update this user'}), 403
    # if the id matches, query for the user info from the id if it exists
    updated_user = User.query.get_or_404(user_id)
    # get the data from the request if request is json body
    data = request.json
    # call the update_user method from the User class and pass in the data
    updated_user.update_user_method(data)
    # return a dictionary of the updated user info
    return jsonify(updated_user.to_dict())


# the DELETE method is used to delete a resource from the server
@api.route('/users/<user_id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(user_id): # similar to th eupdate_user route
    # set a variable as the current_user data
    current_user = token_auth.current_user()
    # if the current_user.id does not match the user_id, that user is not authorized to delete that user
    if current_user.id != int(user_id):
        return jsonify({'error': 'You are not authorized to update this user'}), 403
    # if the id matches, query for the user info from the id if it exists
    del_user = User.query.get_or_404(user_id)
    # since the client is not sending data we just call the delete_user_method
    del_user.delete_user_method() # nothing is passed in but its "self"
    # return a successfully deleted user json response for the client
    return jsonify({'complete': 'User has been deleted from the database'})



############## SUGGESTION ROUTES ##############

# get all of the suggestions and convert the data into a json response
@api.route('/suggestions', methods= ["GET"])
def get_suggestions():

    suggestions = Suggestion.query.all()
    return jsonify([s.to_dict() for s in suggestions]) # list comprehension 
    # to_dict for every suggestion in suggestions 



# get one suggestion and convert the data into a json response
@api.route('/suggestions/<suggestion_id>')
@token_auth.login_required # user must be logged in to view a suggestion
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
    for field in ['activity', 'category', 'participants', 'price', 'link', 'user_id']: ## COME BACK AND REMOVE 'USER_ID'
        if field not in data:

            # if field not in request body, return error
            return jsonify({'error': f'<{field}> must be in request body'}), 400

    # if data validated get fields from data dict
    activity = data.get('activity')
    category = data.get('category')
    participants = data.get('participants')
    price = data.get('price')
    link = data.get('link')
    user_id = data.get('user_id') ## REMOVE THIS LINE
    # user = token_auth.current_user() ## UNCOMMENT THIS LINE OUT
    # user_id = user.id ## AND UNCOMMENT THIS LINE

    # create a new instance of suggestion with data
    new_suggestion = Suggestion(activity=activity, category=category, 
        participants=participants, price=price, link=link, user_id=user_id)

    return jsonify(new_suggestion.to_dict()), 201 # 201 is (created), the request
    # succeeded and a new resource was created as a result



# update a suggestion
@api.route('/suggestions/<suggestion_id>', methods=['PUT'])
# @token_auth.login_required ### uncomment out later
def update_suggestion(suggestion_id):
    # query for the suggestion data from suggestion_id
    suggestion = Suggestion.query.get_or_404(suggestion_id)
    # set the current_user data to variable
    # user = token_auth.current_user()
    # # if the current user's id doesn't match the suggestion's user_id return error
    # if user.id != int(suggestion.user_id):
    #     return jsonify({'error': 'You are not authorized to update this suggestion'}), 403
    # get the data from the request if request is json body
    data = request.json
    # update the suggestion with the request data
    suggestion.update_suggestion_method(data)
    return jsonify(suggestion.to_dict())



# delete a suggestion - similar to the update suggestion
@api.route('/suggestions/<suggestion_id>', methods=['DELETE'])
# @token_auth.login_required ### uncomment out later
def delete_suggestion(suggestion_id):
    suggestion = Suggestion.query.get_or_404(suggestion_id)
    # set the current_user data to variable
    # user = token_auth.current_user()
    # # if the current user's id doesn't match the suggestion's user_id return error
    # if user.id != int(suggestion.user_id):
    #     return jsonify({'error': 'You are not authorized to delete this suggestion'}), 403
    suggestion.delete_suggestion_method() # nothing is passed in but its "self"
    return jsonify({'completed': 'Suggestion has been deleted from the database'})