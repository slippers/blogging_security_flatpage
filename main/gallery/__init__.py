from main import app, db
from .models import Gallery, GalleryTag, GalleryTagRel
from .gallery_admin import GalleryAdmin, GalleryTagAdmin


def  config_gallery_admin(admin):
    admin.add_view(GalleryAdmin(db.session))
    admin.add_view(GalleryTagAdmin(db.session))


db.create_all()
