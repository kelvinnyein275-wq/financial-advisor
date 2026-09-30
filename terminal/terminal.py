from flask import Blueprint, render_template, session, request, redirect, url_for
from ml_engine import financial_context_function, create_financial_prompt, create_chat, financial_advice, client, create_history_prompt
terminal = Blueprint("terminal", __name__, static_folder="static", template_folder="templates")
@terminal.route("/terminal", methods=["GET", "POST"])
def terminal_page():
    if "cluster" not in session:
        return redirect(url_for("scan.scanning"))
    age = session["age"]
    income = session["income"]
    expenses = session["expenses"]
    savings = session["savings"]
    cluster = session["cluster"]
    profile_name = session["profile_name"]
 
    context = financial_context_function(age, income, expenses, savings, cluster, profile_name)
    prompt = create_financial_prompt(context=context)
    chat = create_chat(client=client)
    

    if request.method == "GET": #when user first reaches the page
        session["chat_history"] = []
        advice = financial_advice(chat, prompt)
        session["chat_history"].append({"role": "assistant", "message" : advice})
    if request.method == "POST":
        user_message = request.form["message"].strip()
        if not user_message: #if not True -> if False if not False -> True depends on whether user_message() is an empty string or not
            return render_template("terminal-page.html", chat_history=session["chat_history"])
        session["chat_history"].append({"role" : "user", "message" : user_message})
        history_prompt = create_history_prompt(session["chat_history"])
        response = financial_advice(chat, history_prompt)
        session["chat_history"].append({"role" : "assistant", "message" : "response"})

    return render_template("terminal-page.html", chat_history=session["chat_history"])

   