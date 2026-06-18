
from flask import Blueprint, render_template, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models.user_model import User
from models import db

from flask_login import (
    login_user,
    logout_user,
    login_required
)
from flask import flash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    print("REGISTER ROUTE OPENED")

    if request.method == 'POST':

        print("POST REQUEST RECEIVED")

        try:

            username = request.form['username']

            email = request.form['email']

            password = generate_password_hash(
                request.form['password']
            )

            print(username)
            print(email)

            user = User(
                username=username,
                email=email,
                password=password
            )

            db.session.add(user)

            db.session.commit()

            print("USER SAVED SUCCESSFULLY")

            return redirect('/login')

        except Exception as e:

            print("REGISTER ERROR:")
            print(e)

            return str(e)

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    print("LOGIN PAGE OPENED")

    if request.method == 'POST':

        print("LOGIN ATTEMPT")

        try:

            email = request.form['email']

            password = request.form['password']

            print(email)

            user = User.query.filter_by(
                email=email
            ).first()

            if user:

                print("USER FOUND")

                if check_password_hash(
                    user.password,
                    password
                ):
                    
                    print("PASSWORD CORRECT")

                    login_user(user)
                    flash(
                         "Login successful!",
                         "success"
                    )
                    return redirect('/dashboard')

                else:

                    print("WRONG PASSWORD")

                    return "Wrong Password"

            else:

                print("USER NOT FOUND")

                return "User Not Found"

        except Exception as e:

            print("LOGIN ERROR:")
            print(e)

            return str(e)

    return render_template('login.html')
@auth_bp.route('/logout')

@login_required
def logout():

    logout_user()

    return redirect('/login')
