"""Flask application factory."""
from flask import Flask
from .config import Config
from .extensions import bcrypt, csrf, db, limiter, login_manager, mail, migrate, scheduler, server_session


def create_app(config_object: type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"
    csrf.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    server_session.init_app(app)
    limiter.init_app(app)

    from .auth.routes import auth_bp
    from .dashboard.routes import dashboard_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)

    @app.after_request
    def add_security_headers(response):
        for header, value in app.config["SECURITY_HEADERS"].items():
            response.headers.setdefault(header, value)
        response.headers.setdefault("Content-Security-Policy", "default-src 'self' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; font-src 'self' https://cdnjs.cloudflare.com; img-src 'self' data:")
        return response

    with app.app_context():
        import app.auth.models  # noqa: F401
        import app.logs.models  # noqa: F401
    return app
