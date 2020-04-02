from flask import redirect, url_for, flash
from flask_login import UserMixin, current_user
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash

from app import login, db
from app.auth import bp
from app.util import natural_keys


class UnauthorisedAccessError(Exception):
    """ User does not have access priviledges """


@bp.app_errorhandler(UnauthorisedAccessError)
def handle_login_error(e):
    """Redirect to the login page when LoginError is raised."""

    flash("You do not have sufficient access rights to perform this action", 
          'error')
    return redirect(url_for('auth.login'))


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))
        

user_permissions = db.Table('user_permissions',
                            db.Column('user_id', 
                                      db.Integer, 
                                      db.ForeignKey('users.id',
                                                    ondelete='CASCADE'),
                                      index=True),
                            db.Column('permission_id', 
                                      db.Integer, 
                                      db.ForeignKey('permission_groups.id',
                                                    ondelete='CASCADE'),
                                      index=True)
                            )


user_departments = db.Table('user_departments',
                            db.Column('user_id', 
                                      db.Integer, 
                                      db.ForeignKey('users.id',
                                                    ondelete='CASCADE'),
                                      index=True),
                            db.Column('department_id', 
                                      db.Integer, 
                                      db.ForeignKey('departments.id',
                                                    ondelete='CASCADE'),
                                      index=True)
                            )


class PermissionGroups(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(200))
    
    def __repr__(self):
        return '<Permission Group {}: {}>'.format(self.name, 
                                                  self.description)
    
    @staticmethod
    def get_all_groups():
        groups = PermissionGroups.query.all()
        groups.sort(key=lambda x: x.group_name)
        return groups


class Users(UserMixin, db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_authorised = db.Column(db.Boolean)
    is_icu_trained = db.Column(db.Boolean)
    
    access_groups = db.relationship(
                        'PermissionGroups', secondary=user_permissions,
                        backref=db.backref('allowed_users', lazy='dynamic'), 
                        lazy='dynamic')
    
    department_groups = db.relationship(
                        'Departments', secondary=user_departments,
                        backref=db.backref('allowed_users', lazy='dynamic'), 
                        lazy='dynamic')
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def add_access(self, access_group):
        """
        Add new access group priviledge to user
        """
        if not self.has_auth_access(access_group):
            self.access_groups.append(access_group)
    
    def remove_access(self, access_group):
        """
        Remove access group priviledge from the user
        """
        if self.has_auth_access(access_group):
            self.access_groups.remove(access_group)
            
    def add_department_access(self, department):
        """
        Associate user with a deparment
        """
        if department not in self.department_groups:
            self.department_groups.append(department)
        
    def remove_department_access(self, department):
        if department in self.department_groups:
            self.department_groups.remove(department)
    
    def has_auth_access(self, access_groups):
        """
        Check if user is a member of one of the required access groups.
        """
        
        return self.access_groups.filter(
                            user_permissions.c.permission_id.in_(access_groups)
                            ).count() > 0
    
    def has_dept_access(self, dept_id):
        """
        Check whether user has authorisation to make edits to this department
        """
        
        master_access = (PermissionGroups.query
                                         .filter_by(group_name='Master')
                                         .first())
        
        if self.has_auth_access(master_access):
            return True
        
        return self.department_groups.filter(
                            user_departments.c.department_id == int(dept_id)
                            ).count() > 0
    
    @staticmethod
    def get_user_permissions():
        
        permissions = Users.query.all()
        permissions.sort(key=lambda x: natural_keys(x.username))
        return permissions
    

def check_user_group(required_groups):
    """
    Check that user has at least one of the required access groups
    """
    if current_user.is_anonymous:
        raise UnauthorisedAccessError
    
    required_groups.append('Master')
    
    PG = PermissionGroups
    required_access_ids = (db.session.query(PG.id)
                                     .filter(PG.name.in_(required_groups))
                                     .all())
    
    access = current_user.has_auth_access(required_access_ids) 

    if not any(access):
        raise UnauthorisedAccessError

        
def group_required(*groups):
    """
    Decorate a function to require the user to have at least one of the groups.
    """

    def decorator(func):
        @wraps(func)
        def check_auth(*args, **kwargs):
            check_user_group(*groups)

            return func(*args, **kwargs)

        return check_auth

    return decorator