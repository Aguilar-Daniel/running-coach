from flask import Flask
from app.config import CONFIG_MAP
from app.extensions import db, migrate, jwt, bcrypt
from app.errors import register_error_handlers


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(CONFIG_MAP[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    from app import auth_callbacks
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    register_error_handlers(app)

    return app
