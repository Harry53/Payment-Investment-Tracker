"""Authentication routes."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from app.auth.forms import ChangePasswordForm, ForgotPasswordForm, LoginForm, RegisterForm, ResetPasswordForm
from app.auth.models import User
from app.auth.services import create_user, is_locked, record_failed_login, record_successful_login
from app.extensions import db, limiter

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter((User.email == form.email.data.lower()) | (User.username == form.username.data)).first():
            flash("Email or username already exists.", "danger")
        else:
            user = create_user(form)
            flash("Account created. Please verify your email before sensitive actions.", "success")
            login_user(user)
            return redirect(url_for("dashboard.index"))
    return render_template("auth/register.html", form=form)

@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per minute")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if not user or is_locked(user) or not user.check_password(form.password.data):
            if user and not is_locked(user):
                record_failed_login(user)
            flash("Invalid credentials or account locked.", "danger")
        else:
            record_successful_login(user)
            login_user(user, remember=form.remember.data)
            return redirect(request.args.get("next") or url_for("dashboard.index"))
    return render_template("auth/login.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been signed out.", "info")
    return redirect(url_for("auth.login"))

@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        flash("If the email exists, a reset link has been sent.", "info")
        return redirect(url_for("auth.login"))
    return render_template("auth/forgot_password.html", form=form)

@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    user = User.verify_token(token, "reset-password")
    if not user:
        flash("Invalid or expired reset token.", "danger")
        return redirect(url_for("auth.forgot_password"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Password reset complete.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password.html", form=form)

@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash("Current password is incorrect.", "danger")
        else:
            current_user.set_password(form.password.data)
            db.session.commit()
            flash("Password changed.", "success")
    return render_template("auth/profile.html", form=form)
