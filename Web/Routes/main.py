from flask import request, render_template, redirect, url_for, Blueprint, abort
from flask_login import login_required, current_user
from Web.Services.CRUDMethods import create_user, get_all_users, update_user, delete_user
from Web import db
from Web.Models.Users import User
from functools import wraps

main = Blueprint('main', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role_id != 1:  # Giả sử role_id 1 là admin
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


@main.route('/home')
def home():
    return render_template('Extends/home.html')


@main.route('/usermanager')
@login_required
def usermanager():
    # Lấy danh sách người dùng và truyền vào template
    listUser, error = get_all_users()
    if error:
        print('Có lỗi xảy ra khi lấy danh sách người dùng!', error)
        return "Lỗi khi lấy danh sách người dùng"
    return render_template('Extends/UserManager/index.html', ds=listUser)


@main.route('/usermanager/add', methods=['POST', 'GET'])
@login_required
@admin_required
def usermanager_add():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        phone_number = request.form['phone_number']

        # Tạo user mới thông qua phương thức CRUD
        new_user, error = create_user(name, age, phone_number)
        
        if error:
            print('Có lỗi xảy ra khi thêm người dùng!', error)
            return render_template('Extends/UserManager/Add.html')
        
        listUser, error = get_all_users()
        if error:
            print('Có lỗi xảy ra khi lấy lại danh sách người dùng!', error)
            return "Lỗi khi lấy lại danh sách người dùng"
        
        return render_template('Extends/UserManager/index.html', ds=listUser)
    
    return render_template('Extends/UserManager/Add.html')


@main.route('/usermanager/edit/<int:id>', methods=['POST', 'GET'])
@login_required
@admin_required
def usermanager_edit(id):
    # Lấy thông tin người dùng hiện tại từ cơ sở dữ liệu
    user = User.query.get_or_404(id)
    
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        name = request.form['name']
        age = request.form['age']
        phone_number = request.form['phone_number']
        
        updated_user, error = update_user(user, name, age, phone_number)
        
        if error:
            print('Có lỗi xảy ra khi cập nhật thông tin người dùng!', error)
            return render_template('Extends/UserManager/Edit.html', user=user)
        
        return redirect(url_for('main.usermanager'))
    
    return render_template('Extends/UserManager/Edit.html', user=user)


@main.route('/delete/<int:id>')
@login_required
@admin_required
def usermanager_delete(id):
    user = User.query.get_or_404(id)
    
    # Xóa người dùng thông qua phương thức CRUD
    success, error = delete_user(user)
    if error:
        print('Có lỗi xảy ra khi xóa người dùng!', error)
        return "Có lỗi xảy ra khi xóa người dùng!"
    
    return redirect('/usermanager')
