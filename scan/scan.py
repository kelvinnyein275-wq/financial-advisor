from flask import Blueprint, render_template, url_for, redirect, request, session, flash
from ml_engine import cluster_predictions
scan = Blueprint("scan", __name__, static_folder="static", template_folder="templates")

@scan.route("/scan", methods=["POST", "GET"])
def scanning():
    if request.method == "POST":
        age = float(request.form["age"])
        if age < 1 or age > 120:
            flash("Please enter a valid age.")
            return redirect(url_for("scan.scanning"))
        session["age"] = age
        income = float(request.form["income"])
        savings = float(request.form["savings"])
        expenses = float(request.form["expenses"])
        if income < 0 or savings < 0 or expenses < 0:
            flash("Financial values cannot be negative.")
            return redirect(url_for("scan.scanning"))
        session["income"] = income
        session["savings"] = savings
        session["expenses"] = expenses
        cluster = cluster_predictions(age, income, expenses, savings)
        session["cluster"] = int(cluster)
        flash("Succesfully entered info!")
        return redirect(url_for("profile.profiling_page"))
    else:
        return render_template("scan-page.html")
    