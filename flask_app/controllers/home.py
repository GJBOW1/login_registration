from flask import render_template,redirect,request,session,flash
from flask_app import app
from flask_app.models.user import User
from flask_app.controllers import users
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route ('/')
def home():
    # if session.get["user_id"]:
    #     return redirect('/dashboard')
    return render_template('index.html')