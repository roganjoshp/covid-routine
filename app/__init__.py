from flask import Flask, current_app

from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_session import Session, SqlAlchemySessionInterface
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from sqlalchemy import MetaData

from config import Config

import os
import platform

# This is required for redirects to work when behind NGinX
from werkzeug.contrib.fixers import ProxyFix

csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()
session = Session()
login = LoginManager()


def disable_button(*args):
    return False


def create_app():
    
    app = Flask(__name__)
    app.config.from_object(Config)
    
    if platform.system() != 'Windows':
        app.wsgi_app = ProxyFix(app.wsgi_app)
    
    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    
    session.init_app(app)
    # Track migrations for setting up the session
    SqlAlchemySessionInterface(app, db, "sessions", "sess_")
    
    login.init_app(app)
    
    # Register blueprints
    from app.home import bp as home
    app.register_blueprint(home, url_prefix='/')
    
    from app.core import bp as core
    app.register_blueprint(core, url_prefix='/core')
    
    from app.auth import bp as authorisation
    app.register_blueprint(authorisation, url_prefix='/auth')
    login.login_view = 'auth.login'
    
    # Allow us to check whether buttons should be enabled
    app.jinja_env.globals.update(disable_button=disable_button)
    
    return app