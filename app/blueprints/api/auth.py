from datetime import datetime
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.models import User

# creating an instance of the HTTPBasicAuth class
basic_auth = HTTPBasicAuth()
# create an instance of HTTPTokenAuth
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(username, password): # this is a callback function
    # checking if the username column has a value of passed in username
    user = User.query.filter_by(username=username).first()

    # if there is a user and the passed in password matches the hashed password
    # in the database then return the user
    if user is not None and user.check_password(password):
        return user
    
    # by default will return None if there is no user


# verify the user has a token 
@token_auth.verify_token
def verify_token(token):
    # finds user with token if exists
    user = User.query.filter_by(token=token).first()
    now = datetime.utcnow()

    # if there is a user with that token and the token is not expired
    if user is not None and user.token_expiration > now:
        return user