"""initial auth and logs schema"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial_auth_logs"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("permissions", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(100), nullable=False, unique=True), sa.Column("description", sa.String(255), nullable=False))
    op.create_table("roles", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(50), nullable=False, unique=True), sa.Column("description", sa.String(255), nullable=False))
    op.create_table("users", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("email", sa.String(255), nullable=False, unique=True), sa.Column("username", sa.String(80), nullable=False, unique=True), sa.Column("password_hash", sa.String(255), nullable=False), sa.Column("first_name", sa.String(80), nullable=False), sa.Column("last_name", sa.String(80), nullable=False), sa.Column("is_active", sa.Boolean(), nullable=False), sa.Column("email_verified", sa.Boolean(), nullable=False), sa.Column("failed_login_attempts", sa.Integer(), nullable=False), sa.Column("locked_until", sa.DateTime(timezone=True)), sa.Column("two_factor_enabled", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("last_login_at", sa.DateTime(timezone=True)))
    op.create_index("ix_users_email", "users", ["email"])
    op.create_index("ix_users_username", "users", ["username"])
    op.create_table("role_permissions", sa.Column("role_id", sa.Integer(), sa.ForeignKey("roles.id"), primary_key=True), sa.Column("permission_id", sa.Integer(), sa.ForeignKey("permissions.id"), primary_key=True))
    op.create_table("user_roles", sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), primary_key=True), sa.Column("role_id", sa.Integer(), sa.ForeignKey("roles.id"), primary_key=True))
    op.create_table("activity_logs", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id")), sa.Column("action", sa.String(120), nullable=False), sa.Column("details", sa.Text(), nullable=False), sa.Column("ip_address", sa.String(45)), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_activity_logs_user_id", "activity_logs", ["user_id"])
    op.create_table("audit_logs", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id")), sa.Column("entity", sa.String(120), nullable=False), sa.Column("entity_id", sa.String(64), nullable=False), sa.Column("change_summary", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_audit_logs_user_id", "audit_logs", ["user_id"])
    op.create_table("error_logs", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("level", sa.String(20), nullable=False), sa.Column("message", sa.Text(), nullable=False), sa.Column("traceback", sa.Text(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))

def downgrade():
    op.drop_table("error_logs"); op.drop_table("audit_logs"); op.drop_table("activity_logs"); op.drop_table("user_roles"); op.drop_table("role_permissions"); op.drop_index("ix_users_username", table_name="users"); op.drop_index("ix_users_email", table_name="users"); op.drop_table("users"); op.drop_table("roles"); op.drop_table("permissions")
