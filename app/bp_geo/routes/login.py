from flask import Blueprint, render_template, request, abort, session, redirect, url_for
from app.bp_geo.models import Admin

login = Blueprint('login', __name__)


@login.route('/', methods=['GET', 'POST'])
def index():
    if session.get('logged_in'):
        return redirect(url_for('admin.index'))

    admin = Admin.objects().first()

    if request.method == 'POST':
        if not admin:
            return abort('there is no admin account')

        pwd = request.form.get('pwd')

        if not admin.auth(pwd):
            return abort('password not match')

        session['logged_in'] = True
        return redirect(url_for('admin.index'))

    return render_template('login/login.html', admin=admin)


@login.route('/create', methods=['POST'])
def create():
    admin = Admin.objects().first()

    if admin:
        return abort('there is already an admin account')

    pwd = request.form.get('pwd')

    if not pwd or len(pwd) < 3:
        return abort('password not in data or too short (min: 3)')

    admin = Admin()
    admin.pwd = pwd
    admin.save()

    session['logged_in'] = True
    return redirect(url_for('login.index'))


@login.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('login.index'))