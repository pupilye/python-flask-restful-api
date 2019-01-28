import sqlite3
from db import db

class UserModel(db.Model):
    # this is right now an API, to interact with user database
    # An API for our app to interact with the database
    # Isolation
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    
    def __init__(self, username, password):
        # self.id = _id # id is a python keyword
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username): # not using self in the function
        return cls.query.filter_by(username=username).first() # SELECT * FROM items WHERE name=name

    @classmethod
    def find_by_id(cls, _id): # not using self in the function
        return cls.query.filter_by(id=_id).first()
