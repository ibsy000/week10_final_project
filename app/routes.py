from app import app

# the routes are different URLS 
@app.route('/')
def index():
    return "<h1>Hello World</h1>" 