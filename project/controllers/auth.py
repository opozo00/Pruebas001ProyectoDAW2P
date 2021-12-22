from flask import Blueprint, Flask , render_template, redirect, url_for, request,flash,jsonify,flash
from flask_mail import Mail, Message
from password_strength import PasswordPolicy
from password_strength import PasswordStats
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from base64 import b64encode

from werkzeug.wrappers import response
from ..models.usuarios import User
from ..models.especies import Especies
from ..models.registros import Registro 
from project import db, mail



auth = Blueprint('auth', __name__)
#politica de seguridad de contraseña
policy = PasswordPolicy.from_names(
    length=8,  # min length: 8
    uppercase=1,  # need min. 2 uppercase letters
    numbers=1,  # need min. 2 digits
    special=2,
    strength=0.66 # need a password that scores at least 0.5 with its entropy bits
)


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
    stats = PasswordStats(password)
    checkpolicy = policy.test(password)
    print(checkpolicy)
    #se agrega el usuario si el correo no existe, en caso de que si exista no se lo agrega y muestra un mensaje de error
    user = User.query.filter_by(email=email).first() 
    if user:
        flash('La dirección de correo electrónico ya existe.')
        return redirect(url_for('auth.signup'))

    #validar seguridad de contraseña desde el backend
    # ejemplo de contraseña segura que el sistema admite --> V3ryG00dPassw0rd?!
    if(email != "" and name != "" and password != "" ):
        if stats.strength() < 0.66:
            print(stats.strength())
            flash("Password not strong enough. Avoid consecutive characters and easily guessed words.")
            return redirect(url_for('auth.signup'))
        else:
            print(stats.strength())

            new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()

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
    descripcion = request.form.get('descripcion')
    imagen = request.files['imagen'].read()
    user_id = current_user.id

    #b64encode(imagen).decode("utf-8")
    parametro = ""
    
    if nombreEspecie and nombreCientifico and ubicacion and descripcion and imagen !=  parametro:
        registro = Especies(nombre=nombreEspecie,nCientifico=nombreCientifico,ubicacion=ubicacion,descripcion=descripcion,imagen=imagen,usuario_id=user_id)
        #print(nombreEspecie,registro)
        db.session.add(registro)
        db.session.commit()
        try:
            todos = User.query.all()
            correos = []
            for t in todos:
                correo = t.email
                correos.append(correo)
            
            msg = Message('INGRESO DE UNA NUEVA ESPECIE', sender="ospozo.op@gmail.com", recipients=["nafreppubauca-6822@yopmail.com","corderorojasaitor6@gmail.com","ospozo.op@gmail.com","mmvm.512@gmail.com"],body=f"Hola usuario, este correo es enviado con el fin de notificarte AITRO Y JOHN que se ha ingresado una nueva especie a la base de datos --> {registro}")
            print(msg)
            mail.send(msg)
        except Exception as e:
            print(f"Error --> {e}")
    else:
        flash('Introduzca los datos necesarios.')
        return redirect(url_for('main.perfil'))
    

    return redirect('/data')

#Data de todas las especies ingresadas por los diferentes usuarios
@auth.route('/data')
@login_required
def retrieveDataList():
    especies = Especies.query.all()
    return render_template('datalist.html',Especies=especies)

#Data de especie en específico por id
@auth.route('/data/<int:id>')
@login_required
def RetrieveEspecie(id):
    especie = Especies.query.filter_by(id=id).first()
    print(especie)
    if especie:
        return render_template('data.html',especie = especie,imagen=b64encode(especie.imagen).decode("utf-8"))
    return f"Especie con id = {id} NO EXISTE"

#Actualización de información de registro de especie en específico por id
@auth.route('/data/<int:id>/update',methods = ['GET','POST'])
@login_required
def update(id):
    especie = Especies.query.filter_by(id=id).first()
    if request.method == 'POST':
        if especie:
            db.session.delete(especie)
            db.session.commit()
 
            nombreEspecie = request.form.get('especie')
            nombreCientifico = request.form.get('cientifico')
            ubicacion = request.form.get('ubicacion')
            descripcion = request.form.get('descripcion')
            imagen = request.form.get('imagen')
            user_id = current_user.id
            especie = Especies(id=id, nombre=nombreEspecie, nCientifico=nombreCientifico, ubicacion = ubicacion,imagen=imagen,usuario_id=user_id,descripcion=descripcion)

            db.session.add(especie)
            db.session.commit()
            return redirect(f'/data/{id}')
        return f"Especie con id = {id} NO EXISTE"
 
    return render_template('update.html', especie = especie)

#Eliminación de especie en específico por id
@auth.route('/data/<int:id>/delete', methods=['GET','POST'])
@login_required
def delete(id):
    especie = Especies.query.filter_by(id=id).first()
    if request.method == 'POST':
        if especie:
            db.session.delete(especie)
            db.session.commit()
            return redirect('/perfil')
 
    return render_template('delete.html')