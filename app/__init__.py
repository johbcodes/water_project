from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_restful import Api
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
jwt = JWTManager()
api = Api()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'connect_args': {'timeout': 20}
    }

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)
    api.init_app(app)

    login_manager.login_view = "main.login"
    login_manager.session_protection = "strong"

    from .models import User, Project, Funding, County, Constituency, Ward, Region, WaterUsage, WaterSource

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints with explicit url_prefix
    from .routes import main
    app.register_blueprint(main, url_prefix='')  # Empty prefix to match root routes

    # Check for auth blueprint (assuming it exists)
    try:
        from .auth import auth
        app.register_blueprint(auth, url_prefix='/auth')
    except ImportError:
        current_app.logger.warning("Auth blueprint not found; skipping registration.")

    from .resources import ProjectResource
    api.add_resource(ProjectResource, '/api/projects', '/api/projects/<int:project_id>')

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)