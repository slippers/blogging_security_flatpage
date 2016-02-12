from main import db
from flask.ext.security import UserMixin, RoleMixin

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

    # __str__ is required by Flask-Admin, so we can have human-readable 
    # values for the Role when editing a User.
    # If we were using Python 2.7, this would be __unicode__ instead.
    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    # __hash__ is required to avoid the exception TypeError: 
    # unhashable type: 'Role' when saving a User
    def __hash__(self):
        return hash(self.name)


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

    # Required for administrative interface
    def __unicode__(self):
        return self.username


