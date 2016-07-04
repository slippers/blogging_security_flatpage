import os
import os.path as op
from flask import url_for
from jinja2 import Markup
from ..gallery import Gallery, GalleryTag
from flask_admin.contrib.sqla import ModelView
from flask_admin import form as admin_form
from flask_login import current_user


# Create directory for file fields to use
file_path = op.join(op.dirname(__file__), 'static')
try:
    os.mkdir(file_path)
except OSError:
    pass

class GalleryAdmin(ModelView):

    column_auto_select_related = True
    column_list = ('thumb', 'path', 'description', 'tags')
    def is_accessible(self):
        return current_user.has_role('admin')

    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''

        return Markup('<img src="%s">' % url_for('static',
            filename=admin_form.thumbgen_filename(model.path)))

    column_formatters = {
            'thumb': _list_thumbnail
            }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
            'path': admin_form.ImageUploadField('Image',
                base_path=file_path,
                thumbnail_size=(100, 100, True))
            }

    def __init__(self, session):
        # Just call parent class with predefined model.
        super(GalleryAdmin, self).__init__(Gallery, session)


class GalleryTagAdmin(ModelView):

    # Prevent administration of Roles unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')

    def __init__(self, session):
        # Just call parent class with predefined model.
        super(GalleryTagAdmin, self).__init__(GalleryTag, session)


