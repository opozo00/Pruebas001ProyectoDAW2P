from flask_login import UserMixin
from project import db

class Especies(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer)
    nombre = db.Column(db.String(100))
    nCientifico = db.Column(db.String(100))
    ubicacion = db.Column(db.String(100))
    imagen = db.Column(db.LargeBinary)
    #sonido = db.Column(db.LargeBinary)

    def __init__(self,id,nombre,nCientifico,ubicacion,imagen,usuario_id):
        self.id = id
        self.nombre = nombre
        self.nCientifico = nCientifico
        self.ubicacion = ubicacion
        self.imagen = imagen
        self.usuario_id = usuario_id
    
    def __publicacion__(self,nombre,nCientifico,ubicacion,imagen,usuario_id):
        self.nombre = nombre
        self.nCientifico = nCientifico
        self.ubicacion = ubicacion
        self.imagen = imagen
        self.usuario_id = usuario_id
 
    def __repr__(self):
        return f"{self.nombre}:{self.id}"