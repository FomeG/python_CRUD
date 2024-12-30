from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from Web.Models.Users import User
from Web import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu không đúng!')
            
    return render_template('Extends/login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))