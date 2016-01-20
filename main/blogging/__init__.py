from main import app, db
from main.security import security, user_datastore
from flask.ext.blogging import SQLAStorage, BloggingEngine

# configure the bloggin storeage for the blog.db
# using multiple database bound to sqlalchemy
storage = SQLAStorage(db=db, bind="blog")

# create all the tables
db.create_all()

# start the blogging engine
blogging_engine = BloggingEngine(app, storage)


# how the blogging engine identifies a user
# pulling user from flask-security user data store
@blogging_engine.user_loader
def load_user(userid):
    print("load_user:",user_datastore.get_user(userid))
    return user_datastore.get_user(userid)

# post configuration
def configure_blogging():
    print("configure:",storage)
