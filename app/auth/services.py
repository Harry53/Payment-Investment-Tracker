"""Authentication business services."""
from datetime import datetime, timedelta, timezone
from flask import request
from flask_mail import Message
from app.auth.models import Role, User
from app.extensions import db, mail
from app.logs.models import ActivityLog

LOCK_THRESHOLD = 5
LOCK_MINUTES = 15

def ensure_default_roles() -> None:
    for name in ("Admin", "User", "Read Only"):
        if not Role.query.filter_by(name=name).first():
            db.session.add(Role(name=name, description=f"{name} access"))
    db.session.commit()

def create_user(form) -> User:
    ensure_default_roles()
    user = User(email=form.email.data.lower(), username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data)
    user.set_password(form.password.data)
    user.roles.append(Role.query.filter_by(name="User").one())
    db.session.add(user)
    db.session.commit()
    log_activity(user.id, "register", "User registered")
    return user

def log_activity(user_id: int | None, action: str, details: str = "") -> None:
    db.session.add(ActivityLog(user_id=user_id, action=action, details=details, ip_address=request.remote_addr if request else None))
    db.session.commit()

def is_locked(user: User) -> bool:
    return bool(user.locked_until and user.locked_until > datetime.now(timezone.utc))

def record_failed_login(user: User) -> None:
    user.failed_login_attempts += 1
    if user.failed_login_attempts >= LOCK_THRESHOLD:
        user.locked_until = datetime.now(timezone.utc) + timedelta(minutes=LOCK_MINUTES)
    db.session.commit()

def record_successful_login(user: User) -> None:
    user.failed_login_attempts = 0
    user.locked_until = None
    user.last_login_at = datetime.now(timezone.utc)
    db.session.commit()
    log_activity(user.id, "login", "Successful login")

def send_token_email(user: User, purpose: str, subject: str, endpoint_url: str) -> None:
    msg = Message(subject=subject, recipients=[user.email], body=f"Open this secure link: {endpoint_url}")
    mail.send(msg)
