import base64
import os
from app import db, login
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin



# Create User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    suggestions = db.relationship('Suggestion', backref='creator', lazy='dynamic')


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # save the user password as the hashed version of the password
        self.set_password(kwargs['password'])
        # save user information to database
        db.session.add(self)
        db.session.commit()


    def __repr__(self):
        return f"<User {self.id} | {self.username}>"


    # function to take in the user password and create a hashed password
    def set_password(self, password):
        self.password = generate_password_hash(password)

    
    # function to check if the given password matches the stored password when
    # user logs in
    def check_password(self, password):
        return check_password_hash(self.password, password)


    # function used to return a dictionary to jsonify
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "date_created": self.date_created,
            "posts": [p.to_dict() for p in self.posts.all()] # this list comprehension returns a list of dictionaries for all the suggestions the user creates
        }


# log in user and get their info from the database
@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Create Suggestion model
class Suggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.String(500), nullable=False, unique=True) # (go for a walk, start a puzzle, etc.)
    category = db.Column(db.String(25), nullable=False) # (random, recreational, friends, couples, etc.)
    participants = db.Column(db.String(10), nullable=False) # (1, 2, 3+, any)
    price = db.Column(db.String(4)) # ($, $$, $$$, $$$$)
    user_id = db.Column(db.String(10), db.ForeignKey('user.id'))


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    
    def __repr__(self):
        return f"<Suggestion {self.id} | {self.activity}"


    # function used to update a user created suggestion
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in {'activity', 'category', 'participants', 'price'}:
                setattr(self, key, value)
        db.session.commit()

    
    # function used to delete a user created suggestion
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    
    # function used to return a dictionary to jsonify
    def to_dict(self):
        return {
            "id": self.id,
            "activity": self.activity,
            "category": self.category,
            "participants": self.participants,
            "price": self.price,
            "user_id": self.user_id
        }