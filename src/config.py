import os
from flask import Flask


class BaseConfig(object):
    SITE_NAME = 'default site name'

    # directory above configure
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    # configuration
    DEBUG = False
    TESTING = False

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_ENGINE = 'sqlite://'

    blog = 'sqlite:///' + os.path.join(basedir, 'database', 'blog.db')
    security = 'sqlite:///' + os.path.join(basedir, 'database', 'security.db')
    gallery = 'sqlite:///' + os.path.join(basedir, 'database', 'gallery.db')

    SQLALCHEMY_BINDS = {
        'blog': blog,
        'security': security,
        'gallery':  gallery,
    }

    # flask-bootstrap
    BOOTSTRAP_USE_MINIFIED = False
    BOOTSTRAP_SERVE_LOCAL = False

    # flask-blogging
    SECRET_KEY = "test a secret"  # for WTF-forms and login
    BLOGGING_URL_PREFIX = "/blog"
    BLOGGING_DISQUS_SITENAME = None
    BLOGGING_FLASK_BOOTSTRAP = True

    # flask-security
    SECURITY_PASSWORD_HASH = "sha512_crypt"
    SECURITY_PASSWORD_SALT = "salty"

    # flask-flatpages
    FLATPAGES_EXTENSION = '.md'
    # FLATPAGES_HTML_RENDERER
    FLATPAGES_MARKDOWN_EXTENSIONS = ['fenced_code']
    FLATPAGES_AUTO_RELOAD = True
    FLATPAGES_ROOT = "content"
    PAGE_DIR = 'pages'


class DevelopmentConfig(BaseConfig):
    SITE_NAME = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_ECHO = False


class TestingConfig(BaseConfig):
    SITE_NAME = 'testing'
    DEBUG = False
    TESTING = True


class ProductionConfig(BaseConfig):
    SITE_NAME = 'production'


config = {
    "development": "src.config.DevelopmentConfig",
    "testing": "src.config.TestingConfig",
    "production": "src.config.ProductionConfig"
}


def configure_app():

    app = Flask(__name__, instance_relative_config=True)

    print("instance path:", app.instance_path)

    config_name = os.getenv('FLAKS_CONFIGURATION', 'development')

    print(config_name, ":",  config[config_name])

    app.config.from_object(config[config_name])

    app.config.from_pyfile(config_name + ".cfg", silent=True)

    # print out config
    if app.config['DEBUG']:
        for key, value in app.config.items():
            print(key, value)

    return app
