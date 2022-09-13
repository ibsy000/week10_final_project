from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS

# the __name__ variable passed in to the Flask class is a predefined variable
# which is set to the name of the module in which it is used
app = Flask(__name__)


# config subclass of a dictionary, from_object will go through class attributes
app.config.from_object(Config)


# Create an instance of SQLAlchemy (the ORM) with the flask application
db = SQLAlchemy(app)

# Create an instance of Migrate which will be the migration engine and pass
# in the app and SQLAlchemy instance
migrate = Migrate(app, db)

# Create an instance of the LoginManager to handle authentication
login = LoginManager(app)

# Cross-Origin Resource Sharing is a mechanism that allows restricted resources 
# on a web page to be requested from another domain outside the domain from 
# which the first resource was served. 
# ex: server is running on localhost:500 and front end running on localhost:3000
CORS(app)

# imports api
from app.blueprints.api import api
# everything that is apart of that api is now part of the app
app.register_blueprint(api)

# routes is always imported at the bottom, this is a workaround to circular imports
# a common problem with Flask applications
from . import routes, models