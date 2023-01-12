# Ioana A Mititean
# Exercise 19.3 - Flask Tools

"""
Main code for survey application - Flask setup, routes, and view functions.
"""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "alt ceva secreta"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


# VIEW FUNCTIONS ----------------------------------------------------------------------------------

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


@app.route("/init_responses", methods=["POST"])
def initialize_responses():
    """
    Initialize an empty list of user responses in the current user session, then redirect to the
    first question of the survey.
    """

    session["responses"] = []
    return redirect("/questions/0")


@app.route("/questions/<int:qnum>")
def display_question(qnum):
    """
    Display the survey question designated by the given integer 'qnum'.
    """

    responses = session.get("responses")

    # If responses not yet initialized, redirect to homepage
    if responses is None:
        flash("Please click 'begin survey' to access the survey.")
        return redirect("/")

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
    Add user response for a survey question to user session and redirect user to next question.
    """

    answer = request.form.get("response")

    responses = session["responses"]
    responses.append(answer)
    session["responses"] = responses

    return redirect(f"/questions/{qnum+1}")


@app.route("/thanks")
def show_thanks():
    """
    Display a thank-you page (for completing the full survey).
    """

    responses = session.get("responses")

    # If responses not yet initialized, redirect to homepage
    if responses is None:
        flash("Please click 'begin survey' to access the survey.")
        return redirect("/")

    questions = satisfaction_survey.questions
    num_answered = len(responses)
    total_questions = len(questions)

    # If survey not complete, redirect to appropriate question page
    if num_answered != total_questions:
        flash("Attempted to access invalid URL.")
        return redirect(f"/questions/{num_answered}")

    # Make a dict of questions and corresponding responses
    ques_dict = dict(zip(questions, session["responses"]))

    return render_template("thanks.jinja2", q_and_res=ques_dict)

# -------------------------------------------------------------------------------------------------
