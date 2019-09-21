import functools
import hashlib
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
import functools
from flaskr.database import DatabaseConnection


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = DatabaseConnection()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.findOne("users", username) is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            encryptedPassword = hashlib.sha256(password.encode('UTF-8'))  # Specify encryption method
            encryptedPasswordToStoreInDB  = encryptedPassword.hexdigest()  # Build password with correct encoding and specified encryption method
            # encryptedPasswordToStoreInDB = encryptedPassword.hexdigest()
            document = {
                "username": username,
                "password": encryptedPasswordToStoreInDB}
            print(type(generate_password_hash(password)))
            db.insert("users", document)

            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(password)
        db = DatabaseConnection()
        error = None
        user = db.findOneExperimental("users", username)
        encryptedPassword = hashlib.sha256(password.encode('UTF-8'))  # Specify encryption method
        encryptedPasswordToStoreInDB = encryptedPassword.hexdigest()
        print(user['password'])
        print(encryptedPasswordToStoreInDB)
        if user is None:
            error = 'Incorrect username.'
        elif not encryptedPasswordToStoreInDB == user['password']:
            print("made it to password check")
            error = 'Incorrect password.'
        else:
            pass

        if error is None:
            session.clear()
            session['user_id'] = user['_id']
            print("we got this far")
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.findAll(user_id)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view