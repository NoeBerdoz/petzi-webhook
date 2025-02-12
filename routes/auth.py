import psycopg2.extras
from flask import render_template, request, redirect, url_for, session, flash, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from persistence.database import Database


auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(f):
    """ Helper function to check if a user is logged in """
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to log in first.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """ Login a user and adds user_id and username key-values in the session dict """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with Database.get_db_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute("SELECT id, password FROM users WHERE username = %s;", (username,))
                user = cur.fetchone()

                if user and check_password_hash(user['password'], password):
                    session['user_id'] = user['id']
                    session['username'] = username
                    flash('Logged in successfully!', 'success')
                    return redirect(url_for('dashboard.get_home'))
                else:
                    flash('Invalid username or password.', 'error')

    return render_template('login.html')


@auth_blueprint.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Déconnecté avec succès !', 'success')
    return redirect(url_for('auth.login'))


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        with Database.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO users (username, password) VALUES (%s, %s);", (username, hashed_password))
                conn.commit()

        flash('Compte créé avec succès ! Merci de te connecter.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_blueprint.route('/settings', methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in
def change_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_new_password = request.form['confirm_new_password']

        # Check if new passwords match
        if new_password != confirm_new_password:
            flash('Les mots de passe ne correspondent pas', 'error')
            return redirect(url_for('auth.change_password'))

        # Fetch the current user's data
        with Database.get_db_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute("SELECT password FROM users WHERE id = %s;", (session['user_id'],))
                user = cur.fetchone()

                # Verify the current password
                if user and check_password_hash(user['password'], current_password):
                    # Hash the new password
                    hashed_password = generate_password_hash(new_password)

                    # Update the password in the database
                    cur.execute("UPDATE users SET password = %s WHERE id = %s;", (hashed_password, session['user_id']))
                    conn.commit()

                    flash('Mot de passe modifié avec succès !', 'success')
                    return redirect(url_for('auth.change_password'))
                else:
                    flash('Le mot de passe actuel donné est incorrect.', 'error')

    return render_template('change_password.html', title="Paramètres utilisateurs")