from main import app, db

# Define models

class Gallery(db.Model):
    __bind_key__ = 'gallery'
    __tablename__ = 'gallery'
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(255))
    path = db.Column(db.String(255))
    tag_id = db.Column(db.Integer(), db.ForeignKey('tags.id'))
    tags = db.relationship('Tag', 
            secondary='gallery_tags',
            backref=db.backref('tags', lazy='dynamic'))

    # __str__ is required by Flask-Admin, so we can have human-readable 
    # If we were using Python 2.7, this would be __unicode__ instead.
    def __str__(self):
        return self.path

    def __unicode__(self):
        return self.path

    # __hash__ is required to avoid the exception TypeError: 
    def __hash__(self):
        return hash(self.path)

class Tag(db.Model):
    __bind_key__ = 'gallery'
    __tablename__ = 'tags'
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.Unicode(64))
    
    def __unicode__(self):
        return self.text

    # __str__ is required by Flask-Admin, so we can have human-readable 
    # If we were using Python 2.7, this would be __unicode__ instead.
    def __str__(self):
        return self.text


class GalleryTags(db.Model):
    __bind_key__ = 'gallery'
    __tablename__ = 'gallery_tags'
    id = db.Column(db.Integer(), primary_key=True)
    gallery_id = db.Column(db.Integer(), db.ForeignKey('gallery.id'))
    tag_id = db.Column(db.Integer(), db.ForeignKey('tags.id'))



