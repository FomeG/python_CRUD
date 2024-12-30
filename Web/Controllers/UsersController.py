from Web import db
from Web.Models.Users import User

# Phương thức tạo người dùng mới
def create_user(name, age, phone_number, role_id=2):
    try:
        new_user = User(
            name=name,
            age=age,
            phone_number=phone_number,
            role_id=role_id
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user, None
    except Exception as e:
        db.session.rollback()
        return None, str(e)

# Phương thức lấy danh sách người dùng
def get_all_users():
    try:
        return User.query.order_by(User.created_at).all(), None
    except Exception as e:
        return None, str(e)

# Phương thức cập nhật thông tin người dùng
def update_user(user, name, age, phone_number):
    try:
        user.name = name
        user.age = age
        user.phone_number = phone_number
        db.session.commit()
        return user, None
    except Exception as e:
        db.session.rollback()
        return None, str(e)

# Phương thức xóa người dùng
def delete_user(user):
    try:
        db.session.delete(user)
        db.session.commit()
        return True, None
    except Exception as e:
        db.session.rollback()
        return False, str(e)
