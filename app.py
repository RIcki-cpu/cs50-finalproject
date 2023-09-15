from flask import Flask, flash, redirect, render_template, request, session

from helperLLM import get_reply_chatbot

# Configure application
app = Flask(__name__)

def set_personality(argument):
    if argument == "Psychologist(Default)":
        return "psychologist"
    elif argument == "Buhdist Monk":
        return "monk"
    elif argument == 3:
        return "Steven Hawking"
    else:
        return "steven_hawking"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the user input
        input_text = request.form.get("user_input")
        temperature_str = request.form.get("temperature")
        personality = request.form.get("personality")
        if temperature_str is not None and temperature_str.isdigit():
            temperature = int(temperature_str)
        else:
            temperature = 0

        answer_dic = get_reply_chatbot(set_personality(personality), input_text, float(temperature/10))
        return render_template("index.html", answer_text=answer_dic["answer"])
    return render_template("index.html")