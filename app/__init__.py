"""Flask application factory."""
from importlib import import_module
from pathlib import Path
from urllib.parse import unquote

from flask import Flask
from .config import Config
from .extensions import bcrypt, csrf, db, limiter, login_manager, mail, migrate, scheduler, server_session


def _ensure_sqlite_parent_directory(database_uri: str) -> None:
    """Create the parent directory for file-based SQLite databases."""
    if not database_uri.startswith("sqlite") or database_uri in {"sqlite://", "sqlite:///:memory:"}:
        return

    if database_uri.startswith("sqlite:////"):
        database = "/" + database_uri.removeprefix("sqlite:////")
    elif database_uri.startswith("sqlite:///"):
        database = database_uri.removeprefix("sqlite:///")
    else:
        return

    database = unquote(database)
    if not database or database == ":memory:":
        return

    database_path = Path(database)
    if not database_path.is_absolute():
        database_path = Path.cwd() / database_path
    database_path.parent.mkdir(parents=True, exist_ok=True)


def create_app(config_object: type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)
    _ensure_sqlite_parent_directory(app.config["SQLALCHEMY_DATABASE_URI"])

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
        import_module("app.auth.models")
        import_module("app.logs.models")
    return app
