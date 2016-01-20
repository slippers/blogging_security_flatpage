from main import app, db
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
        UserMixin, RoleMixin, login_required, roles_accepted
from flask_security.utils import encrypt_password

from flask_login import current_user

# Define models

class RoleUsers(db.Model):
    # save table to security database
    __bind_key__ = 'security'
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id'))

class Role(db.Model, RoleMixin):
    __bind_key__ = 'security'
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    __bind_key__ = 'security'
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', 
            secondary='roles_users', 
            backref=db.backref('users',lazy='dynamic'))
    
    # used by flask-blogging to get name to display on post
    def get_name(self):
        return self.email

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create any database tables that don't exist yet.
db.create_all()

def configure_security():
    # Create the Roles "admin" and "end-user" -- unless they already exist
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='end-user', description='End user')


    # Create two Users for testing purposes -- unless they already exists.
    # In each case, use Flask-Security utility function to encrypt the password.
    pw = encrypt_password('password')
#    pw = 'password'
    if not user_datastore.get_user('someone@example.com'):
        user_datastore.create_user(email='someone@example.com', password=pw)
    if not user_datastore.get_user('admin@example.com'):
        user_datastore.create_user(email='admin@example.com', password=pw)


    # Give one User has the "end-user" role, while the other has the "admin" role. 
    #(This will have no effect if the
    # Users already have these Roles.) Again, commit any database changes.
    user_datastore.add_role_to_user('someone@example.com', 'end-user')
    user_datastore.add_role_to_user('admin@example.com', 'admin')

    db.session.commit()

