from flask import Blueprint, Flask ,render_template
from flask_login import login_required, current_user
from project import db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template("login.html")

@main.route('/perfil')
@login_required
def perfil():
    return render_template("perfil.html", name = current_user.name)