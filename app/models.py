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


# log in user and get their info from the database
@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Create Suggestion model
class Suggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.String(500), nullable=False, unique=True)
    category = db.Column(db.String(25), nullable=False)
    participants = db.Column(db.Integer, nullable=False)
    price = db.Column(db.String(4))


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