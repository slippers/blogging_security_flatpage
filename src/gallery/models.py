from src import app, db


# Define models
class Gallery(db.Model):
    __bind_key__ = 'gallery'
    __tablename__ = 'gallery'
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(255))
    path = db.Column(db.String(255))
#    tag_id = db.Column(db.Integer(), db.ForeignKey('gallery_tag_rel.id'))
    tags = db.relationship('GalleryTag', 
            secondary='gallery_tag_rel',
            backref=db.backref('gallery', lazy='dynamic'))

    # __str__ is required by Flask-Admin, so we can have human-readable 
    # If we were using Python 2.7, this would be __unicode__ instead.
    def __str__(self):
        return self.path

    def __unicode__(self):
        return self.path

    # __hash__ is required to avoid the exception TypeError: 
    def __hash__(self):
        return hash(self.path)

class GalleryTag(db.Model):
    __bind_key__ = 'gallery'
    __tablename__ = 'gallery_tag'
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.Unicode(64), unique=True)
    
    def __unicode__(self):
        return self.text

    # __str__ is required by Flask-Admin, so we can have human-readable 
    # If we were using Python 2.7, this would be __unicode__ instead.
    def __str__(self):
        return self.text


class GalleryTagRel(db.Model):
    __bind_key__ = 'gallery'
    __tablename__ = 'gallery_tag_rel'
    id = db.Column(db.Integer(), primary_key=True)
    gallery_id = db.Column(db.Integer(), db.ForeignKey('gallery.id'))
    tag_id = db.Column(db.Integer(), db.ForeignKey('gallery_tag.id'))



