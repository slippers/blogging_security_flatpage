from main import app
from flask import render_template, redirect
from security import login_required, roles_accepted
from flask_flatpages import FlatPages


flatpages = FlatPages(app)

# errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', title='Page Not Found'), 404

@app.errorhandler(410)
def page_not_found(e):
    return render_template('error.html', title='Page deleted'), 403

@app.errorhandler(403)
def page_not_found(e):
    return render_template('error.html', title='Forbidden'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('error.html', title='Server error'), 500


# Views
@app.route('/')
def home():
    return render_template('index.html', content='home')

@app.route('/index')
@login_required
def index():
    return render_template('index.html',content='index')

@app.route('/profile')
@login_required
def profile():
    return render_template('index.html', content='profile')

@app.route('/admin')
@login_required
@roles_accepted('admin')
def admin():
    return render_template('index.html', content='admin')

@app.route('/admin_or_editor')
@roles_accepted('admin','editor')
@login_required
def admin_or_editor():
    return render_template('index.html', content='admin_or_editor')

@app.route('/pages/<name>')
def page(name):
    """ render static pages """
    path = '{}/{}'.format(app.config.get('PAGE_DIR'), name)
    page = flatpages.get_or_404(path)
    return render_template('page.html', page=page)
