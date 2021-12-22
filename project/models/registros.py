from flask_login import UserMixin
from project import db

class Registro(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer)
    especie_id = db.Column(db.Integer)
    registro = db.Column(db.String(25))
    #comentario = db.Column(db.String(150))