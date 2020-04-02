from flask import (render_template, flash, redirect, url_for, request, jsonify,
                   session, current_app)

from app import db, csrf

from app.auth import bp
from app.auth.models import Users

from flask_login import login_user, logout_user, current_user


def create_default_user():
    """ Check that there is at least one user in the system
    
    If there are no existing users, make a default user and give them Master
    permission. This user can then be used to create another moderator user and
    can then be deleted
    """
    
    users = Users.query.all()
    if not users:
        default_user = Users(username='default')
        default_user.set_password('deleteme')
        db.session.add(default_user)
        db.session.commit()


@bp.route('/login', methods=['POST', 'GET'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('home.homepage'))
    
    if request.method == 'GET':
        print("fired")
        create_default_user()
        return render_template('auth/login.html')
        
    req = request.form.to_dict()
    username = req.get('username')
    password = req.get('password')
    
    user = Users.query.filter_by(username=username).first()

    if user is None:
        return jsonify({'outcome': 'error',
                        'message': 'username or password not recognised'})
    
    if not user.check_password(password):
        return jsonify({'outcome': 'error',
                        'message': 'username or password not recognised'})
    
    login_user(user, remember=True)
    return ""


@bp.route('/request_access', methods=['POST'])
def request_access():
    return ""


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))  