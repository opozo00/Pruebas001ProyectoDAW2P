from flask import Flask
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import psycopg2

#conn = psycopg2.connect("dbname='DAW-app' user='postgres' host='localhost' password='oscarpozo'")
db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    #conn = psycopg2.connect("dbname='DAW-app' user='postgres' host='localhost' password='oscarpozo'")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:oscarpozo@localhost/postgres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = 'oscarpozo@uees.edu.ec' #pueden cambiar por su correo pero aún no funciona del todo
    app.config['MAIL_PASSWORD'] = 'UsuarioChelo463' #tambien usen su contraseña de correo
    app.config['MAIL_PORT'] = 'True'


    db.init_app(app)
    mail.init_app(app)
    # controllers module register
    from .controllers import controllers as controllers_blueprint
    app.register_blueprint(controllers_blueprint)

    #Con Posgres da error
    # models module register
    #from .models import models as models_blueprint
    #app.register_blueprint(models_blueprint)
    
    # blueprint for auth routes in our app
    from .controllers.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .controllers.main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models.models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    


    return app