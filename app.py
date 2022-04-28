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


@app.route("/")
def index():
    return render_template("create-polls.html")


# Function for /register route
# noinspection SpellCheckingInspection
@app.route("/register", methods=['POST', 'GET'])
def register():
    # Connect to the database
    conn = sqlite3.connect('Voting_database.db')
    c = conn.cursor()
    print("yes")
    if request.method == "POST":
        f_name = request.form.get("first_name")
        l_name = request.form.get("last_name")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        re_password = request.form.get("re_password")
        dob = request.form.get("dateofbirth")
        state = request.form.get("state")
        mobile = request.form.get("phone")
        gender = request.form.get("gender")

        # Check if all the fields are filled
        if not (f_name and l_name and username and email and password and re_password and dob and state and mobile and
                gender):
            # print("debug time", gender, "\n", state, "\n", f_name, "\n", l_name, "\n", username, "\n", password, "\n",
                  # re_password, "\n", dob, "\n", mobile)
            error_message = "All the fields in the form must be filled"
            print(error_message)
            return render_template("apology.html", message=error_message)

        if password != re_password:
            error_message = "Passwords do not match"
            print(error_message)
            return render_template("apology.html", message=error_message)

        # Check if username already exists
        c.execute("SELECT * FROM login_creds WHERE username = :user_name", {"user_name": username})
        conn.commit()
        row = c.fetchall()
        if len(row) > 0:
            error_message = "Username is already taken"
            print(error_message)
            return render_template("apology.html", message=error_message)

        # Check if email already exists
        c.execute("SELECT * FROM user_data WHERE Email = :e", {"e": email})
        conn.commit()
        row = c.fetchall()
        if len(row) > 0:
            error_message = "Email_id already exists"
            print(error_message)
            return render_template("apology.html", message=error_message)

        # Generate password hash
        hashed_password = generate_password_hash(password)

        # Insert user data in user_data table
        c.execute("INSERT INTO user_data(First_Name, Last_Name, DOB, State, Mob_Number, Gender, Email)"
                  " VALUES(:f, :l, :d, :s, :p, :g, :e )",
                  {"f": f_name, "l": l_name, "d": dob, "s": state, "p": mobile, "g": gender, "e": email})
        conn.commit()

        # Insert username and password in login_creds table
        c.execute("INSERT INTO login_creds(username, password) VALUES(:u, :p)", {"u": username, "p": hashed_password})
        conn.commit()

        # flash("Registered !!")
        print("Registered !!!!!")
        return render_template("login.html")

    else:
        return render_template("register.html")


@app.route("/login", methods=['POST', 'GET'])
def login():
    conn = sqlite3.connect('Voting_database.db')
    c = conn.cursor()
    # if you are already logged in you cant access the login page
    if session.get("user_id"):
        return render_template("home.html")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("pswd")
        # opt = request.form.get("otp")
        print(password)
        if not (username and password):
            error_message = "Enter username and password"
            print(error_message)
            return render_template("apology.html", message=error_message)

        c.execute("SELECT * FROM login_creds WHERE username = :u ", {"u": username})
        rows = c.fetchone()
        # print(generate_password_hash(password))

        if not check_password_hash(rows[2], password):
            error_message = "Invalid username and password"
            print(error_message)
            return render_template("apology.html", message=error_message)

        session["user_id"] = rows[0]
        return render_template("home.html")

    else:
        return render_template("login.html")


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    session.clear()
    return redirect("/")

@app.route("/create_polls", methods=['POST'])
def create_polls():
    pname = request.form.get("poll_name")
    ques = request.form.get("question")
    options_count = int(request.form.get("options_numbers"))
    poll_type = request.form.get("poll_type")
    poll_range = request.form.get("poll_range")
    gender = request.form.get("gender")
    age = request.form.get("age")
    state = request.form.get("state")

    options = []
    for i in range(8):
        j = (i + 1)
        index = "option"+str(j)
        single_option = request.form.get(index)
        options.append(single_option)
    for option in options:
        if not option:
            print("null here")
        else :
            print(option)


    # Check if all the fields are filled
    if not (pname and ques and options_count and poll_type and poll_range):
        error_message = "All the fields in the form must be filled 1"
        print(error_message)
        return render_template("apology.html", message=error_message)
    for i in range(options_count):
        if not options[i]:
            error_message = "All the fields in the form must be filled 2"
            print(error_message)
            return render_template("apology.html", message=error_message)

        # form date format -> mm/dd/yyyy
        start_date = (poll_range[0:11]).strip()
        expiry_date = (poll_range[13:]).strip()

        # sql date format -> yyyy/mm/dd
        # converting to date from form format to sql date format

        formatted_start_date = datetime.strptime(start_date, '%m/%d/%Y').strftime('%Y/%m/%d')
        formatted_expiry_date = datetime.strptime(expiry_date, '%m/%d/%Y').strftime('%Y/%m/%d')
        pname = pname.strip()
        ques = ques.strip()

        print(pname)
        print(ques)
        print(options_count)
        print(poll_type)
        print(start_date)
        print(expiry_date)
        print(formatted_start_date)
        print(formatted_expiry_date)
        print(gender)
        print(age)
        print(state)

    public = 0
    private = 0
    if poll_type == '1':
        age = 'all'
        gender = 'all'
        state = 'all'
        public = 1
    else:
        private = 1

    age_filter = 0
    if age == '18+':
        age_filter = 1

    conn = sqlite3.connect('Voting_database.db')
    c = conn.cursor()
    # # 420 to be changed to int(session["user_id"]) which is owner's user id
    owner = 420
    zero = 0
    c.execute("INSERT INTO poll_filters(start, end, public, private, no_of_options, age, gender, state)"
              " VALUES(:s, :e, :pu, :pr, :n, :a, :g, :st)",
              {"s": formatted_start_date, "e": formatted_expiry_date, "pu": public, "pr": private, "n": options_count, "a": age_filter,
               "g": gender, "st": state})
    c.execute("INSERT INTO poll_data(owner, pollname, quest, op1, op2, op3, op4, op5, op6, op7, op8)"
              " VALUES(:o, :p, :q, :o1, :o2, :o3, :o4, :o5, :o6, :o7, :o8 )",
              {"o": owner, "p": pname, "q": ques, "o1": options[0], "o2": options[1], "o3": options[2], "o4": options[3], "o5": options[4], "o6": options[5], "o7": options[6], "o8": options[7]})
    c.execute("INSERT INTO poll_results(op1, op2, op3, op4, op5, op6, op7, op8)"
              " VALUES(:o1, :o2, :o3, :o4, :o5, :o6, :o7, :o8 )",
              {"o1": zero, "o2": zero, "o3": zero, "o4": zero, "o5": zero, "o6": zero, "o7": zero, "o8": zero})
    c.execute("SELECT poll_id from poll_data WHERE pollname = :p", {"p": pname})
    poll_id = c.fetchone()
    table_name = "poll_no" + poll_id[0]
    query = """CREATE TABLE {}( userid INTEGER PRIMARY KEY, Option INTEGER ) """.format(table_name)
    c.execute(query)
    conn.commit()
    return redirect("/")



if __name__ == '___main__':
    app.run()
