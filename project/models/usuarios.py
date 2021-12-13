from flask_login import UserMixin
from project import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(100))
    #direccion = db.Column(db.String(150))
    #fNacimiento = db.Column(db.String())
