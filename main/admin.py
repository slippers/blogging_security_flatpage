#https://github.com/sasaporta/flask-security-admin-example/blob/master/main.py

import os
import os.path as op
from flask import url_for
from main import app, db
from flask.ext.login import current_user
from flask_admin import Admin, helpers as admin_helpers, form as admin_form
from flask_security.utils import encrypt_password
from .security import security, RoleUsers, Role, User
from flask_admin.contrib.sqla import ModelView
from wtforms.fields import PasswordField
from jinja2 import Markup
from .gallery import Gallery, Tag


# Create directory for file fields to use
file_path = op.join(op.dirname(__file__), 'static')
try:
    os.mkdir(file_path)
except OSError:
    pass

class GalleryAdmin(ModelView):

    column_auto_select_related = True
    column_list = ('description', 'path', 'tags')
    def is_accessible(self):
        return current_user.has_role('admin')

    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''

        return Markup('<img src="%s">' % url_for('static',
            filename=admin_form.thumbgen_filename(model.path)))

    column_formatters = {
            'path': _list_thumbnail
            }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
            'path': admin_form.ImageUploadField('Image',
                base_path=file_path,
                thumbnail_size=(100, 100, True))
            }



class UserAdmin(ModelView):

    # Don't display the password on the list of Users
    column_exclude_list = ('password',)

    # Don't include the standard password field when creating or editing a User (but see below)
    form_excluded_columns = ('password',)

    # Automatically display human-readable names for the current and available Roles 
    # when creating or editing a User
    column_auto_select_related = True

    # Prevent administration of Users unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')

    # On the form for creating or editing a User, don't 
    # display a field corresponding to the model's password field.
    # There are two reasons for this. First, we want to encrypt the 
    # password before storing in the database. Second,
    # we want to use a password field (with the input masked) rather than a regular text field.
    def scaffold_form(self):

        # Start with the standard form as provided by Flask-Admin. 
        # We've already told Flask-Admin to exclude the
        # password field from this form.
        form_class = super(UserAdmin, self).scaffold_form()

        # Add a password field, naming it "password2" and labeling it "New Password".
        form_class.password2 = PasswordField('New Password')
        return form_class

        # This callback executes when the user saves changes to a 
        # newly-created or edited User -- before the changes are
        # committed to the database.
    def on_model_change(self, form, model, is_created):

        # If the password field isn't blank...
        if len(model.password2):
            # ... then encrypt the new password prior to storing it in the database. 
            # If the password field is blank,
            # the existing password in the database will be retained.
            model.password = encrypt_password(model.password2)


# Customized Role model for SQL-Admin
class RoleAdmin(ModelView):

    # Prevent administration of Roles unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')


admin = Admin(app, 'Administration', template_mode='bootstrap3')
admin.add_view(UserAdmin(User, db.session))
admin.add_view(RoleAdmin(Role, db.session))

admin.add_view(GalleryAdmin(Gallery, db.session))

# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
            )
