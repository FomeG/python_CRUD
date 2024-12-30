from Web import db
from datetime import datetime

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)  # ID tự tăng
    name = db.Column(db.String(50), nullable=False, unique=True)  # Tên vai trò (Admin, User, etc.)
    users = db.relationship('User', backref='role', lazy=True)  # Quan hệ 1-N với User

    def __repr__(self):
        return f"<Role {self.name}>"
