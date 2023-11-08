import ast
from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, session
# from flask_session import Session

# helper methods
from helperLLM import get_reply_chatbot
from helpers import apology, login_required

# mysql and config
from flask_mysqldb import MySQL
from config import config
from flask_wtf.csrf import CSRFProtect

# Models
from models.user_model import UserModel
from models.mood_tracker_model import MoodTrackerModel

# Entities
from models.entities.user import User
from models.entities.mood_record import MoodRecord


# Configure application
app = Flask(__name__)

# Connection to MySQL
db = MySQL(app)

csrf = CSRFProtect()


# This function defines the personality
def set_personality(argument):
    if argument == "Psychologist(Default)":
        return "psychologist"
    elif argument == "Buddhist Monk":
        return "monk"
    elif argument == 3:
        return "Steven Hawking"
    else:
        return "steven_hawking"


# This function set the emoji depending the level of wellbeing
def well_being_emoji(range):
    if 0 <= range <= 2:
        return f'<i class="fa-solid fa-face-sad-tear fa-2xl" style="color: #000000;"></i>'
    elif 3 <= range <= 4:
        return f'<i class="fa-solid fa-face-frown fa-2xl" style="color: #05053d;"></i>'
    elif 5 <= range <= 6:
        return f'<i class="fa-solid fa-face-meh fa-2xl" style="color: #090979;"></i>'
    elif 7 <= range <= 8:
        return f'<i class="fa-solid fa-face-smile fa-2xl" style="color: #056fbc;"></i>'
    elif 9 <= range <= 10:
        return f'<i class="fa-solid fa-face-laugh-beam fa-2xl" style="color: #00d4ff;"></i>'
    else:
        return Exception


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    today = datetime.now()
    response_dic = {}
    user = UserModel.get_by_id(db, session["user_id"])
    response_dic["user_name"] = user.fullname.split()[0]

    if request.method == "POST":
        # Get the user input
        input_text = request.form.get("user_input")
        temperature_str = request.form.get("temperature")
        personality = request.form.get("personality")

        if input_text is None or temperature_str is None or personality is None:
            flash("Complete all input fields")
            return render_template("index.html", response_dic=response_dic)

        # Adding validation to the temperature field
        if temperature_str is not None and temperature_str.isdigit():
            temperature = int(temperature_str)
        else:
            temperature = 0

        # LLM response
        response_dic = get_reply_chatbot(set_personality(personality), input_text, float(temperature / 10))
        print(today)

        # New MoodRecord
        record = MoodRecord(today, response_dic["emotions"], response_dic["wellbeing_level"])

        MoodTrackerModel.add_record(db, session["user_id"], record)

        # Update User Number of Tokens
        UserModel.update_tokens(db, session["user_id"], response_dic["tokens"])

        # add emoji
        response_dic["emoji"] = well_being_emoji(int(response_dic["wellbeing_level"]))

        return render_template("index.html", response_dic=response_dic)
    return render_template("index.html", response_dic=response_dic)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # creates a user
        user = User(0, request.form['username'], request.form['password'])
        # login user
        logged_user = UserModel.login(db, user)

        if logged_user is not None:
            # if the user exits and password match then redirect user to home page
            if logged_user.password:
                # login_user(logged_user)

                # Remember which user has logged in
                session["user_id"] = logged_user.id

                return render_template("index.html", response_dic=None)
            else:
                flash("Invalid password...")
                return render_template('login.html')
        else:
            flash("User not found...")
            return render_template('login.html')

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("login")


@app.route("/register", methods=["GET", "POST"])
def register():
    # Get current Data
    today = datetime.now()
    """Register user"""
    if request.method == "POST":
        username = request.form.get('username')
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        birthday = request.form.get('birthday')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        # Perform custom validation here
        errors = validate_registration_form(username, fullname, email, birthday, password, confirmation)


        if errors:
            for error in errors:
                flash(error + "\n", 'danger')
        else:
            # age calculation
            birthday_arr = birthday.split('-')
            age = today.year - int(birthday_arr[0]) - ((today.month, today.day) < (int(birthday_arr[1]), int(birthday_arr[2])))

            # Check if username already exists and match passwords
            user = User(0, username, password, fullname, email, age)
            if UserModel.login(db, user) is not None:
                return apology("Username already exists")
            elif password != confirmation:
                return apology("Passwords do not match")

            # Perform Registration
            id_new_user = UserModel.register(db, user)

            # Registration is successful, perform further processing
            flash('Registration successful', 'success')

            # Remember which user has logged in
            session["user_id"] = id_new_user

            # Redirect user to home page
            return render_template("index.html", response_dic=None)

    # it means that the user is trying to log in
    return render_template("register.html")


@app.route("/tracker")
@login_required
def display_mood_tracker():
    """Display mood_tracker user"""

    records_dic = []
    # get all records
    records = MoodTrackerModel.retrieve_mood_records(db, session["user_id"])

    # transform MoodRecordObject to Dic
    for record in records:
        # date = datetime.strptime(record.date, '%Y-%m-%d')
        record_dic = {"emotions": ast.literal_eval(record.emotions), "well_being_level": int(record.well_being_level),
                      "emoji_well_level": well_being_emoji(int(record.well_being_level)),
                      "date": record.date.strftime('%B %d, %Y')}
        records_dic.append(record_dic)

    # getting total used_tokens by the user
    user = UserModel.get_by_id(db, session["user_id"])

    return render_template("tracker.html", records=records_dic, tokens=user.used_tokens)

def status_400(error):
    return apology("LogIn or Register First", 400)

def validate_registration_form(username, fullname, email, birthday, password, confirmation):
    errors = []

    # Example custom validation rules (you can add more as needed)
    if not fullname:
        errors.append('Full Name is required')
    if not username:
        errors.append('Username is required')
    if not email:
        errors.append('Email is required')
    if not birthday:
        errors.append('Date of Birth is required')
    if not password:
        errors.append('Password is required')
    if password != confirmation:
        errors.append('Passwords do not match')

    return errors

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(400, status_400)
    app.run(
        host='127.0.0.1',
        port=5001,
        debug=True
    )


