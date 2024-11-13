from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
    app.config['SECRET_KEY'] = 'mysecret'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    from .models import User, Product
    from .routes import main
    app.register_blueprint(main)

    return app

