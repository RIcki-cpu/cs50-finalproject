from flask import Flask, flash, redirect, render_template, request, session
from helperLLM import get_reply_chatbot

from config import config

# Configure application
app = Flask(__name__)

#This function defines the personality
def set_personality(argument):
    if argument == "Psychologist(Default)":
        return "psychologist"
    elif argument == "Buhdist Monk":
        return "monk"
    elif argument == 3:
        return "Steven Hawking"
    else:
        return "steven_hawking"

#This function set the emoji depending the level of wellbeing
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

    response_dic = {} 

    if request.method == "POST":
        # Get the user input
        input_text = request.form.get("user_input")
        temperature_str = request.form.get("temperature")
        personality = request.form.get("personality")

        #Adding validation to the temperature field
        if temperature_str is not None and temperature_str.isdigit():
            temperature = int(temperature_str)
        else:
            temperature = 0

        #LLM response
        response_dic = get_reply_chatbot(set_personality(personality), input_text, float(temperature/10))

        #add emoji
        response_dic["emoji"] = well_being_emoji(int(response_dic["wellbeing_level"]))

        return render_template("index.html", response_dic = response_dic)
    return render_template("index.html", response_dic = response_dic)


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

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5001,
        debug=True
    )