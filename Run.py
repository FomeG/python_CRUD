from Web import create_app, db
from Web.Models.Users import User
from Web.Models.Roles import Role
from werkzeug.security import generate_password_hash
import os

app = create_app()


# with app.app_context():
#         # Xóa tất cả bảng cũ và tạo lại
#     db.drop_all()
#     db.create_all()
    
#     # Kiểm tra và thêm dữ liệu mẫu cho Role
#     if not Role.query.first():
#         admin_role = Role(name='Admin')
#         user_role = Role(name='User')
#         db.session.add(admin_role)
#         db.session.add(user_role)
#         db.session.commit()
    
#     # Kiểm tra và thêm users mẫu
#     if not User.query.first():
#         # Lấy roles từ database
#         admin_role = Role.query.filter_by(name='Admin').first()
#         user_role = Role.query.filter_by(name='User').first()
        
#         # Tạo admin user
#         admin_user = User(
#             name='nghia1',
#             age=30,
#             phone_number='0123456789',
#             username='nghia1',
#             password='123',
#             role_id=admin_role.id
#         )
        
#         # Tạo regular user
#         regular_user = User(
#             name='nghia',
#             age=25,
#             phone_number='0334414209',
#             username='nghia',
#             # password=generate_password_hash('user123'),
#             password='123',
#             role_id=user_role.id
#         )
        
#         # Thêm users vào database
#         db.session.add(admin_user)
#         db.session.add(regular_user)
#         db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)