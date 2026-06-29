from app import create_app
from app.config import TestingConfig
from app.extensions import db
from app.auth.models import User


def test_app_registers_security_headers():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
    client = app.test_client()
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert response.headers['X-Frame-Options'] == 'DENY'


def test_password_hashing_roundtrip():
    app = create_app(TestingConfig)
    with app.app_context():
        user = User(email='a@example.com', username='alice', first_name='Alice', last_name='User')
        user.set_password('very-secure-password')
        assert user.password_hash != 'very-secure-password'
        assert user.check_password('very-secure-password')


def test_sqlite_parent_directory_created(tmp_path, monkeypatch):
    db_file = tmp_path / 'nested' / 'finance.db'

    class LocalConfig(TestingConfig):
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_file}'

    app = create_app(LocalConfig)
    assert app.config['SQLALCHEMY_DATABASE_URI'].endswith(str(db_file))
    assert db_file.parent.exists()
