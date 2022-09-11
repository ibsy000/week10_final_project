from app import app
from flask import render_template, redirect, url_for
from app.forms import LoginForm, RegisterForm

# the routes are different URLS 
@app.route('/')
def index():
    return render_template('index.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    
    
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    return render_template('login.html', form=form)