from logging.config import fileConfig
from alembic import context
from app import create_app
from app.extensions import db

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
app = create_app()
target_metadata = db.metadata

def run_migrations_offline():
    url = app.config["SQLALCHEMY_DATABASE_URI"]
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    with app.app_context():
        connection = db.engine.connect()
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
        connection.close()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
