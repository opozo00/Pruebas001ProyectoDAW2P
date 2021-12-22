from flask_login import UserMixin
from project import db

class Especies(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer)
    nombre = db.Column(db.String(100))
    nCientifico = db.Column(db.String(100))
    ubicacion = db.Column(db.String(100))
    imagen = db.Column(db.LargeBinary)
    descripcion = db.Column(db.String())
    #sonido = db.Column(db.LargeBinary)
    
 
    def __repr__(self):
        return f"{self.nombre}: {self.descripcion}"