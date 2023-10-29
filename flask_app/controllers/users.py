from flask import render_template,redirect,request,session,flash
from flask_app import app
from flask_app.models.user import User
from flask_app.controllers import home
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/register', methods=["POST"])
def register():
    if User.get_by_email(request.form):
        flash("This email is already registered.")
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : pw_hash
    }
    if not User.validate_user(data):
        return redirect('/')
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if not session.get("user_id"):
        return redirect('/')
    data = {
        "id" : session["user_id"]
    }
    logged_user = User.get_by_id(data)
    return render_template('dashboard.html', user = logged_user)

@app.route('/login/user', methods=["POST"])
def login():
    data = {
        "email" : request.form["email"],
        "password" : request.form["password"]
    }
    if not User.validate_user_login(data):
        return redirect('/')
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email and/or Password")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email and/or Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

@app.route('/logout', methods=["POST"])
def logout():
    print(session)
    session.clear()
    print("session is: ", session)
    return redirect('/')