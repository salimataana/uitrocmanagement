from flask import Flask
from flask_login import LoginManager

from auth import auth as auth_blueprint
from main import main as main_blueprint
from database import db

# init SQLAlchemy so we can use it later in our models


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    from models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    from models  import user
    with app.app_context():
        db.create_all()
    return app