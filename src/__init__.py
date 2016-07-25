# from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap, WebCDN
from .config import configure_app

# Create app
app = configure_app()

# Create database connection object
db = SQLAlchemy(app)  # flask-sqlalchemy

# flask-bootstrap
Bootstrap(app)  # flask-bootstrap
bootswatch = WebCDN('//maxcdn.bootstrapcdn.com/bootswatch/3.3.6/spacelab/')
cdns = app.extensions['bootstrap']['cdns']
cdns['bootswatch'] = bootswatch

# import the flask-security feature
from .security import configure_security

# setup all the routes to the views
from .views import *

# create the site navigation for bootstrap to use
from .site_nav import nav

# blogging extention
from .blogging import blogging_engine, configure_blogging

from .admin import admin

# execute before first request is processed
@app.before_first_request
def before_first_request():
    configure_security()
    configure_blogging()
