from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Import models to ensure they are registered with the app context
    from app.models import User, Subject

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.routes.subjects import subjects as subjects_blueprint
    app.register_blueprint(subjects_blueprint)
    
    from app.routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
