# Personal Finance & Wealth Management System

This first increment establishes the production-ready Flask foundation: application factory, blueprints, SQLAlchemy, Flask-Migrate/Alembic integration, Flask-Login, Flask-WTF CSRF, Flask-Bcrypt password hashing, Flask-Mail, Flask-Limiter, server-side sessions, APScheduler readiness, Docker, Nginx, Gunicorn, security headers, dashboard shell, auth flows, logging tables, and the generic spreadsheet import engine.

## Run locally

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
flask --app wsgi.py db init
flask --app wsgi.py db migrate -m "initial schema"
flask --app wsgi.py db upgrade
flask --app wsgi.py run
```

## Development order

1. Foundation, authentication, Docker, and database setup.
2. Bank accounts and transaction tracking.
3. Credit card management.
4. Mutual funds and redemption tracking.
5. Stock trading and portfolio management.
6. Insurance, loans, disputes, analytics, reports, tax, notifications, and email automation.
