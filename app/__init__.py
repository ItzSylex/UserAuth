from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from .utils.database import init_db
import os

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24)
    
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    init_db()
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    return app
