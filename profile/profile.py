from flask import Blueprint, render_template, session, request, redirect, url_for
from ml_engine import profiling, get_cluster_medians
profile = Blueprint("profile", __name__, static_folder="static", template_folder="templates")


@profile.route("/profile")
def profiling_page():
    if "cluster" not in session:
        return redirect(url_for("scan.scanning"))
    cluster = session["cluster"]
    user_profile = profiling(cluster)
    profile_name = user_profile["name"]
    profile_description = user_profile["description"]
    session["profile_name"] = profile_name
    session["profile_description"] = profile_description
    age = session["age"]
    income = session["income"]
    expenses = session["expenses"]
    savings = session["savings"]
    if income > 0:
        savings_rate = round((savings/income) * 100, 1)
        expense_ratio = round((expenses/income) * 100, 1)
    else:
        savings_rate = 0
        expense_ratio = 0
    median_data = get_cluster_medians(cluster)
    median_age = median_data["age"]
    median_income = (float(median_data["income"])/12)
    median_expenses = (float(median_data["expenses"])/12)
    median_savings = (float(median_data["savings"])/12)
    median_savings_rate = round((median_savings/median_income) * 100, 1)
    median_expense_ratio = round((median_expenses/median_income) * 100, 1)

    #dict containing all variables
    financial_context = {
    "age": age,
    "income": income,
    "expenses": expenses,
    "savings": savings,
    "cluster": cluster,
    "profile_name": profile_name,
    "profile_description": profile_description,
    "savings_rate": savings_rate,
    "expense_ratio": expense_ratio,
    "median_age": median_age,
    "median_income": median_income,
    "median_expenses": median_expenses,
    "median_savings": median_savings,
    "median_savings_rate": median_savings_rate,
    "median_expense_ratio": median_expense_ratio
}


    return render_template(
        "profile-page.html",
        profile_name=profile_name, profile_description=profile_description, your_age=age, your_income=income, your_expenses=expenses, your_savings=savings, 
        median_age=median_age, median_income=median_income, median_expenses=median_expenses, median_savings=median_savings,
        savings_rate=savings_rate, median_savings_rate=median_savings_rate, expense_ratio=expense_ratio, median_expense_ratio=median_expense_ratio
    ), financial_context

def get_financial_context():
        cluster = session["cluster"]
        user_profile = profiling(cluster)
        profile_name = user_profile["name"]
        profile_description = user_profile["description"]
        session["profile_name"] = profile_name
        session["profile_description"] = profile_description
        age = session["age"]
        income = session["income"]
        expenses = session["expenses"]
        savings = session["savings"]
        savings_rate = float(savings/income)
        expense_ratio = float(expenses/income)
        median_data = get_cluster_medians(cluster)
        median_age = median_data["age"]
        median_income = (float(median_data["income"])/12)
        median_expenses = (float(median_data["expenses"])/12)
        median_savings = (float(median_data["savings"])/12)
        median_savings_rate = float(median_savings/median_income)
        median_expense_ratio = float(median_expenses/median_income)
    
        #dict containing all variables
        financial_context = {
        "age": age,
        "income": income,
        "expenses": expenses,
        "savings": savings,
        "cluster": cluster,
        "profile_name": profile_name,
        "profile_description": profile_description,
        "savings_rate": savings_rate,
        "expense_ratio": expense_ratio,
        "median_age": median_age,
        "median_income": median_income,
        "median_expenses": median_expenses,
        "median_savings": median_savings,
        "median_savings_rate": median_savings_rate,
        "median_expense_ratio": median_expense_ratio
        }
        return financial_context
    