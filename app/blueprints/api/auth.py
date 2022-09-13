from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.models import User

# creating an instance of the HTTPBasicAuth class
basic_auth = HTTPBasicAuth()


@basic_auth.verify_password
def verify_password(username, password): # this is a callback function
    # checking if the username column has a value of passed in username
    user = User.query.filter_by(username=username).first()

    # if there is a user and the passed in password matches the hashed password
    # in the database then return the user
    if user is not None and user.check_password(password):
        return user
    
    # by default will return None if there is no user



