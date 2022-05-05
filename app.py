import datetime
import re
import sqlite3

from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from tempfile import mkdtemp
from functools import wraps

from helper import convert_date, compare_date

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
    return render_template("welcome.html")


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
        # c.execute("INSERT INTO login_creds(username, password) VALUES(:u, :p)", {"u": username, "p": hashed_password})
        # conn.commit()

        # flash("Registered !!")
        print("Registered !!!!!")
        return render_template("login.html")

    else:
        return render_template("register.html")


@app.route("/login", methods=['POST', 'GET'])
def login():
    conn = sqlite3.connect('Voting_database.db')
    c = conn.cursor()
    # if you are already logged in you can't access the login page
    if session.get("user_id"):
        return redirect("/home")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("pswd")
        # opt = request.form.get("otp")
        print(password)
        # Check if user exists
        if not (username or password):
            error_message = "Enter username and password"
            print(error_message)
            return render_template("apology.html", message=error_message)

        c.execute("SELECT * FROM login_creds WHERE username = :u ", {"u": username})
        rows = c.fetchone()

        # Check if passwords match
        if rows == None or not check_password_hash(rows[2], password):
            error_message = "Invalid username and password"
            print(error_message)
            return render_template("apology.html", message=error_message)

        # Start Session
        session["user_id"] = rows[0]
        return redirect("/home")

    else:
        return render_template("login.html")


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    session.clear()
    return redirect("/")


@app.route("/create_polls", methods=["GET", "POST"])
@login_required
def create_polls():
    # Connect to the database
    conn = sqlite3.connect('Voting_database.db')
    c = conn.cursor()

    if request.method == "POST":
        pname = request.form.get("poll_name")
        ques = request.form.get("question")
        options_count = int(request.form.get("options_numbers"))
        poll_type = request.form.get("poll_type")
        poll_range = request.form.get("poll_range")
        gender = request.form.get("gender")
        age = request.form.get("age")
        state = request.form.get("state")
        email = request.form.get("email_list")

        options = []
        for i in range(8):
            j = (i + 1)
            idx = "option"+str(j)
            single_option = request.form.get(idx)
            options.append(single_option)

        # Check if emails are valid
        e_list = email.split("\r\n")
        valid_mails = []
        invalid_mails = []
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        for mail in e_list:
            if re.fullmatch(email_pattern, mail):
                valid_mails.append(mail)
            else:
                invalid_mails.append(mail)

        # Delete extra list
        del e_list

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

        formatted_start_date = datetime.datetime.strptime(start_date, '%m/%d/%Y').strftime('%Y/%m/%d')
        formatted_expiry_date = datetime.datetime.strptime(expiry_date, '%m/%d/%Y').strftime('%Y/%m/%d')
        pname = pname.strip()
        ques = ques.strip()

        public = 0
        private = 0
        #poll_type == 1 means public
        #poll_type == 2 means private
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

        # Insert data into the database
        owner = int(session["user_id"])
        zero = 0
        c.execute("INSERT INTO poll_filters(start, end, public, private, no_of_options, age, gender, state)"
                  " VALUES(:s, :e, :pu, :pr, :n, :a, :g, :st)",
                  {"s": formatted_start_date, "e": formatted_expiry_date, "pu": public, "pr": private,
                   "n": options_count, "a": age_filter, "g": gender, "st": state})
        c.execute("INSERT INTO poll_data(owner, pollname, quest, op1, op2, op3, op4, op5, op6, op7, op8)"
                  " VALUES(:o, :p, :q, :o1, :o2, :o3, :o4, :o5, :o6, :o7, :o8 )",
                  {"o": owner, "p": pname, "q": ques, "o1": options[0], "o2": options[1], "o3": options[2],
                   "o4": options[3], "o5": options[4], "o6": options[5], "o7": options[6], "o8": options[7]})
        c.execute("INSERT INTO poll_results(op1, op2, op3, op4, op5, op6, op7, op8)"
                  " VALUES(:o1, :o2, :o3, :o4, :o5, :o6, :o7, :o8 )",
                  {"o1": zero, "o2": zero, "o3": zero, "o4": zero, "o5": zero, "o6": zero, "o7": zero, "o8": zero})
        if private == 1:
            c.execute("SELECT pollid from poll_data WHERE pollname = :p", {"p": pname})
            poll_id = c.fetchone()
            table_name = "poll_no" + str(poll_id[0])
            query = """CREATE TABLE {}( userid INTEGER PRIMARY KEY, Option INTEGER ) """.format(table_name)
            c.execute(query)
        conn.commit()
        conn.close()

        # Only valid mails added invalid mails not added. Flash message on home page later that these mails
        # have not been added

        for mail in valid_mails:
            query = """ INSERT INTO {}(emailid, option) VAlUES(:m, :o) """.format(table_name)
            c.execute(query, {"m": mail, "o": 0})

        return redirect("/home")
    else:
        return render_template("create_polls.html")


@app.route("/home", methods=["GET"])
@login_required
def home():
    return render_template("home.html")


@app.route("/public_polls", methods=["GET", "POST"])
@login_required
def view_public_polls():
    # Connect to the database
    conn = sqlite3.connect('Voting_database.db')
    c = conn.cursor()
    if request.method == "POST":
        print("POST")
        val_0 = request.form.get("part")
        val_1 = request.form.get("res")
        conn = sqlite3.connect('Voting_database.db')
        c = conn.cursor()
        if val_0:
            poll_id = val_0
            c.execute("""SELECT no_of_options FROM poll_filters WHERE pollid = :p""", {"p": poll_id})
            option_count = c.fetchone()[0]
            c.execute("""SELECT * FROM poll_data WHERE pollid = :p """, {"p": poll_id})
            row = c.fetchone()
            conn.commit()
            # print("Participate = " + val_0)
            return render_template("participate.html", arr=row, n=option_count)
        else:
            poll_id = val_1
            c.execute("""SELECT no_of_options FROM poll_filters WHERE pollid = :p""", {"p": poll_id})
            option_count = c.fetchone()[0]
            c.execute("""SELECT * FROM poll_results JOIN poll_data USING (pollid) WHERE pollid = :p """, {"p": poll_id})
            row = c.fetchone()
            conn.commit()
            # print("Result = " + val_1)
            return render_template("result.html", arr=row, n=option_count)
    else:
        # Can optimize this code. Its 3:24 AM and i am tooo lazyyyyyyyyyyyyyy rn
        # Get the data to be displayed from the database
        print("GET")
        c.execute("""SELECT pollid from poll_filters WHERE public == 1""")
        poll_id = c.fetchall()
        poll_name = []
        poll_dates = []
        for idx in poll_id:
            c.execute("""SELECT pollname from poll_data WHERE pollid == :p""", {"p": idx[0]})
            poll_name.append(c.fetchone())
            c.execute("""SELECT start, end from poll_filters WHERE pollid == :p""", {"p": idx[0]})
            poll_dates.append(c.fetchone())

        curr_date = datetime.date.today()
        final_data = []

        # Organize data into a single list
        # Check if poll has expired
        for i in range(len(poll_dates)):
            data = [poll_id[i][0], poll_name[i][0], convert_date(poll_dates[i][0]), convert_date(poll_dates[i][1])]
            # Convert Starting data from yyyy/mm/dd to 4 April
            if not compare_date(poll_dates[i][0]):
                data.append(0)
            else:
                # Convert Ending data from yyyy/mm/dd to 4 April
                data.append(1)
            final_data.append(data)

        print(final_data)
        # Delete extra lists
        del poll_id
        del poll_name
        del poll_dates
        # voted = []
        # for id in poll_id:
        #     table_name = "poll_no" + id
        #     query = """SELECT option from TABLE {}""".format(table_name)
        #     query += " WHERE "
        #     c.execute("""  """)

        return render_template("public_polls.html", data=final_data, n=len(final_data))


@app.route("/private_polls", methods=["GET", "POST"])
@login_required
def private_polls():
    conn = sqlite3.connect('Voting_database.db')
    c = conn.cursor()
    if request.method == "POST":
        val_0 = request.form.get("part")
        val_1 = request.form.get("res")
        if val_0:
            poll_id = val_0
            c.execute("""SELECT no_of_options FROM poll_filters WHERE pollid = :p""", {"p": poll_id})
            option_count = c.fetchone()[0]
            c.execute("""SELECT * FROM poll_data WHERE pollid = :p """, {"p": poll_id})
            row = c.fetchone()
            conn.commit()
            # print("Participate = " + val_0)
            return render_template("participate.html", arr=row, n=option_count)
        else:
            poll_id = val_1
            c.execute("""SELECT no_of_options FROM poll_filters WHERE pollid = :p""", {"p": poll_id})
            option_count = c.fetchone()[0]
            c.execute("""SELECT * FROM poll_results JOIN poll_data USING (pollid) WHERE pollid = :p """, {"p": poll_id})
            row = c.fetchone()
            conn.commit()
            # print("Result = " + val_1)
            return render_template("result.html", arr=row, n=option_count)
    else:
        c.execute("""SELECT email from user_data WHERE userid = :u """, {"u": session["user_id"]})
        email = c.fetchone()[0]
        c.execute("""SELECT pollid from poll_filters WHERE private == 1""")
        poll_id = c.fetchall()

        final_p = []
        final_options = []
        # Check if user has access to the poll if yes then add to final_p and final_options
        for idx in poll_id:
            table_name = "poll_no" + str(idx[0])
            c.execute("""SELECT option from {} where emailid == :o """.format(table_name), {"o": email})
            option = c.fetchone()
            print(option)
            if option is not None:
                final_p.append(idx[0])
                final_options.append(option[0])

        poll_name = []
        poll_dates = []

        for idx in final_p:
            c.execute("""SELECT pollname from poll_data WHERE pollid == :p""", {"p": idx})
            poll_name.append(c.fetchone())
            c.execute("""SELECT start, end from poll_filters WHERE pollid == :p""", {"p": idx})
            poll_dates.append(c.fetchone())

        curr_date = datetime.date.today()
        final_data = []

        # Organize data into a single list
        # Check if poll has expired
        for i in range(len(final_p)):
            # [pollid, poll_name, start_date, end_date, option_selected, date_valid_or_not]
            data = [final_p[i], poll_name[i][0], convert_date(poll_dates[i][0]), convert_date(poll_dates[i][1]),
                    final_options[i]]
            # Convert Starting data from yyyy/mm/dd to 4 April
            if not compare_date(poll_dates[i][0]):
                data.append(0)
            else:
                # Convert Ending data from yyyy/mm/dd to 4 April
                data.append(1)
            final_data.append(data)
        # print(final_data)

        return render_template("private_polls.html", data=final_data, n=len(final_data))


@app.route("/participate", methods=["GET", "POST"])
@login_required
def participate():
    if request.method == "POST":
        # Connect to the database
        print("THIS ONE")
        conn = sqlite3.connect('Voting_database.db')
        c = conn.cursor()
        poll_id = request.form.get("submit")
        option = request.form.get("option")
        c.execute("SELECT private FROM poll_filters WHERE pollid = :p",{"p": poll_id})
        private = str(c.fetchone()[0])
        print("option = "+option)
        print("poll id = "+poll_id)
        if private == "1":
            user_id = session["user_id"]
            print("user id = "+str(user_id))
            c.execute("SELECT email FROM user_data WHERE userid = :u ", {"u": user_id})
            email = c.fetchone()[0]
            print("email = "+email)
            table_name = "poll_no" + poll_id
            print(table_name)
            query = """SELECT option from {} where emailid == :e """.format(table_name)
            print(query)
            c.execute(query, {"e": email})
            opv = str(c.fetchone()[0])
            print(opv)
            if opv[0] != "0":
                print("HERE")
                return redirect("/home")
            c.execute("""UPDATE {} SET option = :o WHERE emailid == :e""".format(table_name), {"o": option, "e": email})
            conn.commit()
        opx = "op" + option
        query = "UPDATE poll_results SET " + opx + " = " + opx + " + 1 WHERE pollid = :p"
        c.execute(query, {"p":poll_id})
        conn.commit()
        return redirect("/home")
    else:
        return redirect("/home")


if __name__ == '___main__':
    app.run()
