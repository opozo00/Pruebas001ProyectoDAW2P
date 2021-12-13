from flask import Blueprint, Flask , render_template, redirect, url_for, request,flash,jsonify
from flask_mail import Mail, Message

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
#from project.models.especies import Especies
from base64 import b64encode

from werkzeug.wrappers import response
#from project.models.registros import Registro
from ..models.models import User
from ..models.especies import Especies
from ..models.registros import Registro 
from project import db, mail



auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template("login.html")

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = request.form.get('remember')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash('Compruebe sus datos de inicio de sesión e inténtelo de nuevo..')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.perfil'))



@auth.route('/signup')
def signup():
    return render_template("signup.html")

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name').lower()
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() 
    if user:
        flash('La dirección de correo electrónico ya existe.')
        return redirect(url_for('auth.signup'))

    if(email != "" and name != "" and password != "" ):
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        msg = Message('PRUEBA 1', sender="oscarpozo@uees.edu.ec", recipients=['ospozo.op@gmail.com'])
        print(msg)
        #mail.send(msg)
    else:
        flash('Introduzca los datos necesarios.')
        return redirect(url_for('auth.signup'))
    

    

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@auth.route('/perfil', methods=['POST'])
@login_required
def registro_especie():
 
    nombreEspecie = request.form.get('especie')
    nombreCientifico = request.form.get('cientifico')
    ubicacion = request.form.get('ubicacion')
    imagen = request.form.get('imagen')
    #audio = request.form.get('audio')
    user_id = current_user.id
    
    #parametro = ""
    registro = Especies.__publicacion__(nombre=nombreEspecie,nCientifico=nombreCientifico,ubicacion=ubicacion,imagen=imagen,usuario_id=user_id)
    print(nombreEspecie,registro)
    db.session.add(registro)
    db.session.commit()
    #if ((nombreEspecie and nombreCientifico and ubicacion and imagen) !=  parametro):
        #registro = Especies(nombre=nombreEspecie,nCientifico=nombreCientifico,ubicacion=ubicacion,imagen=imagen,usuario_id=user_id)
        #print(nombreEspecie,registro)
        #db.session.add(registro)
        #db.session.commit()
    #else:
        #flash('Introduzca los datos correctos.')
        #return redirect(url_for('main.perfil'))
    #print(registro)

    return redirect(url_for('main.perfil'))

@auth.route('/data')
def retrieveDataList():
    especies = Especies.query.all()
    print(especies)
    return render_template('datalist.html',Especies=especies)

@auth.route('/data/<int:id>')
def RetrieveEspecie(id):
    especie = Especies.query.filter_by(id=id).first()
    print(especie)
    if especie:
        #especie = especie
        return render_template('data.html',especie = especie)
    return f"especie with id ={id} Doenst exist"

@auth.route('/data/<int:id>/update',methods = ['GET','POST'])
def update(id):
    especie = Especies.query.filter_by(id=id).first()
    if request.method == 'POST':
        if especie:
            db.session.delete(especie)
            db.session.commit()
 
            nombreEspecie = request.form.get('especie')
            nombreCientifico = request.form.get('cientifico')
            ubicacion = request.form.get('ubicacion')
            imagen = request.form.get('imagen')
            user_id = current_user.id
            especie = Especies(id=id, nombre=nombreEspecie, nCientifico=nombreCientifico, ubicacion = ubicacion,imagen=imagen,usuario_id=user_id)
 
            db.session.add(especie)
            db.session.commit()
            return redirect(f'/data/{id}')
        return f"Especie with id = {id} Does not exist"
 
    return render_template('update.html', especie = especie)

@auth.route('/data/<int:id>/delete', methods=['GET','POST'])
def delete(id):
    especie = Especies.query.filter_by(id=id).first()
    if request.method == 'POST':
        if especie:
            db.session.delete(especie)
            db.session.commit()
            return redirect('/perfil')
        #abort(404)
 
    return render_template('delete.html')