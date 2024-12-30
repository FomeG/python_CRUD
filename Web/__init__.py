from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Web.Config import Config_db
from flask_login import LoginManager




db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config_db)
    
    import os
    app.config['SECRET_KEY'] = os.urandom(24)
    
    db.init_app(app)
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Vui lòng đăng nhập để truy cập trang này!'
    
    
    # Import và đăng ký blueprints
    from Web.Routes.auth import auth
    from Web.Routes.main import main
    
    app.register_blueprint(auth)
    app.register_blueprint(main)
    
    
    from Web.Models.Users import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    
    return app