"""Dashboard routes."""
from flask import Blueprint, render_template
from flask_login import login_required

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
@login_required
def index():
    kpis = {
        "Total Bank Balance": 0, "Total Credit Outstanding": 0, "Net Worth": 0,
        "Investment Value": 0, "Mutual Fund Value": 0, "Trading Portfolio": 0,
        "Insurance Premium": 0, "Loan Outstanding": 0, "Dispute Amount": 0,
        "Upcoming Payments": 0, "Monthly Expense": 0, "Monthly Income": 0, "Monthly Savings": 0,
    }
    return render_template("dashboard/index.html", kpis=kpis)
