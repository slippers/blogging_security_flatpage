from src import app
from flask_admin import Admin, helpers as admin_helpers
from .gallery import config_gallery_admin
from .security import security, config_security_admin


admin = Admin(app, 'Administration', template_mode='bootstrap3')
config_security_admin(admin)
config_gallery_admin(admin)

# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
            )
