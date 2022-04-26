import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from functools import wraps


app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/login", methods=['POST', 'GET'])
def login():
    #asdas
    print("yes")


@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        re_password = request.form.get("re_password")
        f_name = request.form.get("f_name")
        l_name = request.form.get("l_name")
        gender = request.form.get("acc_type")



    else:
        return render_template("register.html")


@app.route("/")
def index():
    return render_template("login.html")


if __name__ == '___main__':
    app.run()
