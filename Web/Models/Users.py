from Web import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = True)
    age = db.Column(db.Integer, nullable = True)
    phone_number = db.Column(db.String(15), nullable = True)
    username = db.Column(db.String(100), nullable = True)
    password = db.Column(db.String(100), nullable = True)
    created_at = db.Column(db.DateTime, default = datetime.now)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable = False)

    def __repr__(self):
        return f"<User: {self.name}>"
    