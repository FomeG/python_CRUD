from flask import jsonify, request, render_template, redirect, url_for, Blueprint, abort
from flask_login import login_required, current_user
from Web.Services.CRUDMethods import create_user, get_all_users, update_user, delete_user
from Web import db
from Web.Models.Users import User
from functools import wraps

from flask_sqlalchemy import pagination

main = Blueprint('main', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role_id != 1:  # role_id 1 là admin
            return "Bạn không có quyền truy cập trang này!"
        return f(*args, **kwargs)
    return decorated_function


@main.route('/home')
def home():
    return render_template('Extends/home.html')



@main.route('/usermanager')
@login_required
def usermanager():
    # Get the page number from the query string (defaults to 1 if not provided)
    page = request.args.get('page', 1, type=int)
    
    # Define how many items per page (e.g., 10 users per page)
    per_page = 10
    
    # Query users with pagination
    listUser = User.query.order_by(User.created_at).paginate(page=page, per_page=per_page, error_out=False)
    
    # Return the template with paginated data
    return render_template('Extends/UserManager/index.html', ds=listUser)


@main.route('/usermanager/search')
@login_required
def usermanager_search():
    # Get the page number from the query string (defaults to 1 if not provided)
    page = request.args.get('page', 1, type=int)
    
    # Define how many items per page (e.g., 10 users per page)
    per_page = 10
    
    query = request.args.get('q', '').lower()
    
    listUser = User.query.filter(
        (User.name.ilike(f"%{query}%")) | 
        (User.phone_number.ilike(f"%{query}%"))
    ).paginate(page=page, per_page=per_page, error_out=False)  # Filter users
    
    # Render a partial template with filtered data
    return render_template('Extends/UserManager/UserList.html', users=listUser)




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




