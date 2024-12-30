from flask import jsonify, request, render_template, redirect, url_for, Blueprint, abort
from flask_login import login_required, current_user
from Web.Controllers.UsersController import create_user, get_all_users, update_user, delete_user
from Web import db
from Web.Models.Users import User
from functools import wraps

from flask_sqlalchemy import pagination

main = Blueprint('main', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role_id != 1:
            return "Bạn không có quyền truy cập trang này!"
        return f(*args, **kwargs)
    return decorated_function

@main.route('/home')
def home():
    return render_template('Extends/home.html')

@main.route('/usermanager')
@login_required
def usermanager():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Use select specific columns instead of all columns
    listUser = User.query.order_by(User.created_at).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('Extends/UserManager/index.html', ds=listUser)

@main.route('/usermanager/search')
@login_required 
def usermanager_search():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    query = request.args.get('q', '').lower()
    
    # Optimize query by selecting specific columns and adding index
    listUser = User.query.filter(
        (User.name.ilike(f"%{query}%")) | 
        (User.phone_number.ilike(f"%{query}%"))
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('Extends/UserManager/UserList.html', users=listUser)

@main.route('/usermanager/add', methods=['POST', 'GET'])
@login_required
@admin_required
def usermanager_add():
    if request.method == 'POST':
        try:
            new_user, error = create_user(
                request.form['name'],
                request.form['age'], 
                request.form['phone_number']
            )

            if error:
                return render_template('Extends/UserManager/Add.html')
        
            return redirect(url_for('main.usermanager'))
    
        except Exception as e:
            print(f'Error adding user: {str(e)}')
            return render_template('Extends/UserManager/Add.html')

    return render_template('Extends/UserManager/Add.html')

@main.route('/usermanager/edit/<int:id>', methods=['POST', 'GET'])
@login_required
@admin_required
def usermanager_edit(id):
    user = User.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            updated_user, error = update_user(
                user,
                request.form['name'],
                request.form['age'],
                request.form['phone_number'] 
            )
            if error:
                return render_template('Extends/UserManager/Edit.html', user=user)
                
            return redirect(url_for('main.usermanager'))
            
        except Exception as e:
            print(f'Error updating user: {str(e)}')
            return render_template('Extends/UserManager/Edit.html', user=user)
    
    return render_template('Extends/UserManager/Edit.html', user=user)

@main.route('/delete/<int:id>')
@login_required
@admin_required
def usermanager_delete(id):
    user = User.query.get_or_404(id)
    
    try:
        success, error = delete_user(user)
        if error:
            abort(500)
        return redirect(url_for('main.usermanager'))

    except Exception as e:
        print(f'Error deleting user: {str(e)}')
        abort(500)
