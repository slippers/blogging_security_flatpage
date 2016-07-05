# blogging_security_flatpage

this is an attept to gather together several popular flask extentions into one application.

combine these flask packages with a single bootstrap default layout. 
* flask-sqlalchemy
* flask-security
* flask-blogging
* flask-nav
* flask-flatpage
* flask-bootstrap
* flask-admin

### configuration

main/config.py contains the configuration logic.
looks for env var FLAKS_CONFIGURATION with name of environment
testing, development, production are the current environments.
if a config file name environment.cfg it will load last

### security

* flask-security handels the users and roles and authentication
* the security module creates some default roles and users if they don't already exits.
* accounts are stored in sparate db file.
* the admin pages have a user and roles list/view/edit form

### database

the blog content and security content is separated in two different sqlalchemy binds.
defaulting to using sqlite
"blog" binding is passed to the flask_blogging for model mangement
"security" binding is passed to the security module where authentication and models reside.

### navigation

the bootstrap navigation is controlled by site_nav which uses the flask_nav extention.
using an inheritance model to control authenticated menu.
the navigation macro is declared in the base.html bootstrap

### flatpages

using flask_flatpage where static md file are rendered into the site and navigation when routed.
flatpages are found in the site_nav where the routes are defined and then serviced by the view.
there is a static content folder where the static files are found.

### admin

flask_admin is a web interface to manage models.
flask_admin uses its own tightly bound bootstrap so this is where the integration falls apart.
in admin we are gaining access to the models of roles, users where they can be edited.

# future

meld the flask_bootstrap, flask_nav with flask_blogging and push back to flask_blogging

meld flask_blogging, flask_nav with flask_admin

add a gallery  
* access in admin
* link to local images in blog editor and display
* generate thumbnails for blog list



