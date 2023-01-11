# Ioana A Mititean
# Exercise 19.3 - Flask Tools

"""
Main code for survey application - Flask setup, routes, and view functions.
"""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "alt ceva secreta"
debug = DebugToolbarExtension(app)

responses = []  # Stores user responses to questions


@app.route("/")
def survey_home():
    """
    Display a page showing survey instructions and a button that starts the survey.
    """

    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template("survey_home.jinja2",
                           survey_title=title,
                           survey_instructions=instructions)


@app.route("/questions/<int:qnum>")
def display_question(qnum):
    """
    Display the survey question designated by the given integer 'qnum'.
    """

    try:
        question = satisfaction_survey.questions[qnum]
    except IndexError:
        return redirect("/thanks")

    text = question.question
    choices = question.choices

    return render_template("survey_question.jinja2",
                           qnum=qnum,
                           qtext=text,
                           qchoices=choices)


@app.route("/answers", methods=["POST"])
def add_answer():
    """
    Add user response for a survey question to a response list and redirect user to next question.
    """

    answer = request.form.get("response")
    responses.append(answer)

    return redirect("/questions/0")


@app.route("/thanks")
def show_thanks():
    """
    Display a thank-you page (for completing the full survey).
    """

    return render_template("thanks.jinja2")
