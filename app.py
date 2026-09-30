from flask import Flask, redirect, render_template, url_for
from scan.scan import scan
from profile.profile import profile
from terminal.terminal import terminal


app = Flask(__name__)
app.register_blueprint(scan, url_prefix="/scan")
app.register_blueprint(profile, url_prefix="/profile")
app.register_blueprint(terminal, url_prefix="/terminal")

app.secret_key = "financial-app-secret-key"

if __name__ == "__main__":
    app.run(debug=True)