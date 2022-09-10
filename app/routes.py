from app import app
from flask import render_template, redirect, url_for

# the routes are different URLS 
@app.route('/')
def index():
    return render_template('index.html')