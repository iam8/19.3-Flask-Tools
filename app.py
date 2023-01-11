# Ioana A Mititean
# Exercise 19.3 - Flask Tools

"""
Main code for survey application - Flask setup, routes, and view functions.
"""

from flask import Flask, request, render_template
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
