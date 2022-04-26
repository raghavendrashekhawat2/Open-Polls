import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
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
    conn = sqlite3.connect('Voting_database.db')
    c = conn.cursor()
    return render_template("login.html")


# Function for /register route
# noinspection SpellCheckingInspection
@app.route("/register", methods=['POST', 'GET'])
def register():
    # Connect to the database
    conn = sqlite3.connect('Voting_database.db')
    c = conn.cursor()
    print("yes")
    if request.method == "POST":
        f_name = request.form.get("f_name")
        l_name = request.form.get("l_name")
        username = request.form.get("username")
        password = request.form.get("password")
        re_password = request.form.get("re_password")
        dob = request.form.get("dateofbrith")
        state = request.form.get("state")
        mobile = request.form.get("phone")
        gender = request.form.get("gender")

        print("debug time", gender, "\n", state, "\n", f_name, "\n", l_name, "\n", username, "\n", password, "\n", re_password, "\n", dob, "\n", mobile)

        # Check if all the fields are filled
        if not (f_name and l_name and username and password and re_password and dob and state and mobile and gender):
            error_message = "All the fields in the form must be filled"
            print(error_message)
            return render_template("apology.html", message=error_message)
        if password != re_password:
            error_message = "Passwords do not match"
            print(error_message)
            return render_template("apology.html", message=error_message)

        # Check if username already exists
        c.execute("SELECT * FROM users WHERE user_name = :user_name", {"user_name": username})
        conn.commit()
        row = c.fetchall()
        if len(row) > 0:
            error_message = "Username is already taken"
            print(error_message)
            return render_template("apology.html", message=error_message)

        # Generate password hash
        hashed_password = generate_password_hash(password)

        # Insert user data in user_data table
        c.execute("INSERT INTO user_data(First_Name, Last_Name, DOB, State, Mob_Number, gender)"
                  " VALUES(:f, :l, :d, :s, :p, :g )",
                  {"f": f_name, "l": l_name, "d": dob, "s": state, "p": mobile, "g": gender})
        conn.commit()

        # Insert username and password in login_creds table
        c.execute("INSET INTO login_cred(username, password) VALUES(:u, :p"), {"u": username, "p": hashed_password}
        conn.commit()

        # flash("Registered !!")
        print("Registered !!!!!")
        return render_template("login.html")

    else:
        return render_template("register.html")


@app.route("/")
def index():
    return render_template("login.html")


if __name__ == '___main__':
    app.run()
