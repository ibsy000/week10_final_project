from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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


# routes is always imported at the bottom, this is a workaround to circular imports
# a common problem with Flask applications
from . import routes