# Ioana A Mititean
# Exercise 19.3 - Flask Tools

"""
Main code for survey application - Flask setup, routes, and view functions.
"""

from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "alt ceva secreta"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

responses = []  # Stores user responses to questions


# VIEW FUNCTIONS ----------------------------------------------------------------------------------

@app.route("/")
def survey_home():
    """
    Display a page showing survey instructions and a button that starts the survey.
    """

    num_answered = len(responses)
    total_questions = len(satisfaction_survey.questions)

    # If survey already completed, redirect to thank-you page
    if num_answered == total_questions:
        flash("Survey already completed!")
        return redirect("/thanks")

    # If user survey is in progress, redirect to the appropriate survey question
    if (0 < num_answered < total_questions):
        flash("Error - survey is in progress!")
        return redirect(f"/questions/{num_answered}")

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

    num_answered = len(responses)
    total_questions = len(satisfaction_survey.questions)

    # If all questions answered, redirect to thank you page
    if num_answered == total_questions:
        flash("Survey complete!")
        return redirect("/thanks")

    # Redirect to appropriate question if user manually types in non-current question URL
    if qnum != num_answered:
        flash("Attempted to access invalid URL.")
        return redirect(f"/questions/{num_answered}")

    question = satisfaction_survey.questions[qnum]
    text = question.question
    choices = question.choices

    return render_template("survey_question.jinja2",
                           qnum=qnum,
                           qtext=text,
                           qchoices=choices)


@app.route("/answers/<int:qnum>", methods=["POST"])
def add_answer(qnum):
    """
    Add user response for a survey question to a response list and redirect user to next question.
    """

    answer = request.form.get("response")
    responses.append(answer)

    return redirect(f"/questions/{qnum+1}")


@app.route("/thanks")
def show_thanks():
    """
    Display a thank-you page (for completing the full survey).
    """

    num_answered = len(responses)
    total_questions = len(satisfaction_survey.questions)

    # If survey not started, redirect back to homepage
    if not num_answered:
        flash("Attempted to access invalid URL.")
        return redirect("/")

    # If survey not complete, redirect to appropriate question page
    if num_answered != total_questions:
        flash("Attempted to access invalid URL.")
        return redirect(f"/questions/{num_answered}")

    return render_template("thanks.jinja2")

# -------------------------------------------------------------------------------------------------
