import os

class BaseConfig(object):
    SITE_NAME = 'default site name'
    
    # directory above configure 
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    # configuration
    DEBUG = False
    TESTING = False

    SQLALCHEMY_ECHO = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #SQLALCHEMY_DATABASE_URI

    SQLALCHEMY_ENGINE = 'sqlite://'

    SQLALCHEMY_BINDS = {
            'blog': 'sqlite:///' + os.path.join(basedir,'database', 'blog.db'),
            'security': 'sqlite:///' + os.path.join(basedir,'database', 'security.db')
            }


    # flask-blogging
    SECRET_KEY = "test a secret"  # for WTF-forms and login
    BLOGGING_URL_PREFIX = "/blog"
    BLOGGING_DISQUS_SITENAME = None 
    BLOGGING_SITEURL = "http://localhost:8000"
    
    # flask-security
    SECURITY_PASSWORD_HASH = "sha512_crypt"
    SECURITY_PASSWORD_SALT = "salty"

    # flask-flatpages

    FLATPAGES_EXTENSION = '.md'
    #FLATPAGES_HTML_RENDERER
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


config = {
        "development": "main.config.DevelopmentConfig",
        "testing": "main.config.TestingConfig",
        "default": "main.config.DevelopmentConfig"
        }

def configure_app(app):
    config_name = os.getenv('FLAKS_CONFIGURATION', 'default')
    print(config[config_name])
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.cfg', silent=True)

    if config_name == 'default':
        for key,value in app.config.items():
            print(key,value)
