from main import app, db
from .models import User, Role, RoleUsers
from .security_admin import UserAdmin, RoleAdmin
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    login_required, roles_accepted
from flask_security.utils import encrypt_password


def config_security_admin(admin):
    admin.add_view(UserAdmin(db.session))
    admin.add_view(RoleAdmin(db.session))

def configure_security():
    # Create the Roles "admin" and "end-user" -- unless they already exist
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='end-user', description='End user')
    user_datastore.find_or_create_role(name='blogger', description='Blogger')


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
    user_datastore.add_role_to_user('someone@example.com', 'blogger')
    user_datastore.add_role_to_user('admin@example.com', 'admin')
    user_datastore.add_role_to_user('admin@example.com', 'blogger')
    
    db.session.commit()

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create any database tables that don't exist yet.
db.create_all()

