from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from config import configure_app

# Create app
app = Flask(__name__)

configure_app(app)

# Create database connection object
db = SQLAlchemy(app) #flask-sqlalchemy
bs = Bootstrap(app) #flask-bootstrap

#import the flask-security feature
from security import configure_security

import views

# blogging extention
from blogging import blogging_engine, configure_blogging


# execute before first request is processed
@app.before_first_request
def before_first_request():
    configure_security()
    configure_blogging()


