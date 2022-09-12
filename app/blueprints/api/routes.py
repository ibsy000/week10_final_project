from . import api
from flask import jsonify, request
from app.models import Suggestion, User


# get all of the suggestions and convert the data into a json response
@api.route('/suggestions', methods= ["GET"])
def get_suggestions():

    suggestions = Suggestion.query.all()
    return jsonify([s.to_dict() for s in suggestions]) # list comprehension 
    # to_dict for every suggestion in suggestions 



# get one suggestion and convert the data into a json response
@api.route('/suggestions/<suggestion_id>')
def get_suggestion(suggestion_id):

    # query either returns a suggestion if it exists or 404 if it does not exist
    suggestion = Suggestion.query.get_or_404(suggestion_id) # the .get method searches by primary key
    return jsonify(suggestion.to_dict())



# create a suggestion with a post request
@api.route('/suggestions', methods=["POST"])
def create_suggestion():

    # if request is not a json body
    if not request.is_json: # send back a tuple that's a json reponse with a 400 status code
        return jsonify({'error': 'Your request content-type must be application/json'}), 400

    # get the data from the request body
    data = request.json

    # validate the data
    for field in ['activity', 'category', 'participants', 'price', 'user_id']:
        if field not in data:

            # if field not in request body, return error
            return jsonify({'error': f'<{field}> must be in request body'}), 400

    # if data validated get fields from data dict
    activity = data.get('activity')
    category = data.get('category')
    participants = data.get('participants')
    price = data.get('price')
    user_id = data.get('user_id')

    # create a new instance of suggestion with data
    new_suggestion = Suggestion(activity=activity, category=category, 
        participants=participants, price=price, user_id=user_id)

    return jsonify(new_suggestion.to_dict()), 201



# get one user by id and convert the data into a json response
@api.route('/users/<user_id>')
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())