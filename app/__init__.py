from flask import Flask

# the __name__ variable passed in to the Flask class is a predefined variable
# which is set to the name of the module in which it is used
app = Flask(__name__)




# routes is always imported at the bottom, this is a workaround to circular imports
# a common problem with Flask applications
from . import routes