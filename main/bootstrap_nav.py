from main import app
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup

nav = Nav()

@nav.navigation()
def mynavbar():
    return Navbar(app.config.get('SITE_NAME'), 
            View('Home', 'home'),
            View('About', 'page', name='about'),
            Subgroup(
                'Apps',
                View('Product A','page', name='producta'),
                View('Product B','page', name='productb'),

                ),
            )

    # ...

nav.init_app(app)
