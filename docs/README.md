# Personal Finance & Wealth Management System

This first increment establishes the production-ready Flask foundation: application factory, blueprints, SQLAlchemy, Flask-Migrate/Alembic integration, Flask-Login, Flask-WTF CSRF, Flask-Bcrypt password hashing, Flask-Mail, Flask-Limiter, server-side sessions, APScheduler readiness, Docker, Nginx, Gunicorn, security headers, dashboard shell, auth flows, logging tables, and the generic spreadsheet import engine.

The project is designed for Python 3.13 in production. For developer machines that have not upgraded yet, packaging also supports Python 3.12 so setup does not fail before dependencies are installed.

## Process 1: Run with a local Python virtual environment

Use this process when you want to run the app directly on a server or developer machine without Docker.

```bash
cd /var/www/html/Payment-Investment-Tracker
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e '.[dev]'
mkdir -p instance
flask --app wsgi.py db upgrade
flask --app wsgi.py run --host 0.0.0.0 --port 5000
```

Open the app at `http://SERVER_IP:5000/auth/register` and create the first user. The local SQLite database file is created at `instance/finance.db`, not `app/instance/finance.db`.

### Why this fixes the install error

The editable install previously failed with `Multiple top-level packages discovered in a flat-layout` because setuptools saw folders such as `nginx`, `migrations`, and `sample_templates` beside the Python `app` package. The packaging configuration now explicitly includes only `app*`, so `python -m pip install -e '.[dev]'` installs dependencies such as `Flask-Bcrypt` and enables `flask db` commands.

### Useful local commands

```bash
flask --app wsgi.py db current
flask --app wsgi.py db upgrade
python -m pytest
```

Do not run `flask db init` for this repository because the `migrations/` directory is already included. Use `flask db upgrade` to create or update the database schema. If you edited `.env`, make sure `DATABASE_URL` is `sqlite:///instance/finance.db` for a local install; an absolute Docker-only path such as `sqlite:////app/instance/finance.db` can fail on a host server when `/app/instance` does not exist.

## Process 2: Run with Docker Compose

Use this process when you want an isolated production-like runtime with Gunicorn behind Nginx.

```bash
cd /var/www/html/Payment-Investment-Tracker
cp .env.example .env
docker compose build
docker compose up -d

# If your server has the legacy Compose v1 binary instead:
docker-compose build
docker-compose up -d
```

Open the app at `http://SERVER_IP:8080/auth/register`.

The Docker image uses Python 3.13, installs the project package, runs `flask --app wsgi.py db upgrade` automatically on container start, then launches Gunicorn. SQLite data is stored at `/app/instance/finance.db` inside the container on the `sqlite_data` Docker volume and application logs are stored in the `app_logs` Docker volume.

### Useful Docker commands

```bash
docker compose logs -f web
docker compose exec web flask --app wsgi.py db current
docker compose exec web ls -lh /app/instance/finance.db
docker compose exec web python -m pytest
docker compose down

# Legacy Compose v1 equivalents:
docker-compose logs -f web
docker-compose exec web flask --app wsgi.py db current
docker-compose exec web ls -lh /app/instance/finance.db
docker-compose down
```

## Development order

1. Foundation, authentication, Docker, and database setup.
2. Bank accounts and transaction tracking.
3. Credit card management.
4. Mutual funds and redemption tracking.
5. Stock trading and portfolio management.
6. Insurance, loans, disputes, analytics, reports, tax, notifications, and email automation.
