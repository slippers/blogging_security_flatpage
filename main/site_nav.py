from main import app
from flask.ext.login import current_user
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup

nav = Nav()

@nav.navigation()
def mynavbar():
    return Navbar(app.config.get('SITE_NAME'), 
            View('Home', 'home'),
            View('Blog', 'blogging.index'),
            View('About', 'page', name='about'),
            Subgroup(
                'Apps',
                View('Product A','page', name='producta'),
                View('Product B','page', name='productb'),
                ),
            )


@nav.navigation()
def secnavbar():
    secnav = list(mynavbar().items)
    
    if current_user.is_authenticated:
        secnav.extend([
                View('Blog Editor', 'blogging.editor'),
                View('Profile', 'profile'),
                ])

        if current_user.has_role('admin'):
            secnav.append(
                    View('Admin','admin.index')
                    )

        secnav.append(View('Log out', 'security.logout'))
 
    else:
        secnav.append( 
                View('Log in', 'security.login')
                )

    return Navbar(app.config.get('SITE_NAME'), *secnav)

nav.init_app(app)
