from urllib import response
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import SURVEYS as SURVEYS

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"
SURVEY_KEY = "survey"

@app.get("/")
def user_choose_survey():
     """Allow user to choose from list of surveys"""
     return render_template("survey_choice.html", surveys = SURVEYS)

@app.post("/")
def render_survey_start():
    """Displays survey title and start on the page"""
    survey = request.form["survey"]
    session[SURVEY_KEY] = survey
    print(survey)
    return render_template(
        "survey_start.html",
        title=survey.title,
        instructions=survey.instructions)


@app.post("/begin")
def redirect_question_one():
    """Redirect to first question"""

    session[RESPONSES_KEY] = []
    return redirect("/question/0")


@app.get("/question/<int:next_question>")
def show_next_question(next_question):
    """Displays current question and input"""

    responses_length = len(session[RESPONSES_KEY])
    survey = session[SURVEY_KEY]

    if responses_length != next_question:
        flash("Please answer a valid question")
        return redirect(f"/question/{responses_length}")

    if responses_length == len(survey.questions):
        return redirect("/completion")

    question = survey.questions[next_question]
    return render_template("question.html", question=question)


@app.post("/answer")
def redirect_answer():
    """Redirect to next question store answer in RESPONSES"""

    responses = session[RESPONSES_KEY]
    responses.append(request.form["answer"])
    session[RESPONSES_KEY] = responses

    next_question = len(responses)
    return redirect(F"/question/{next_question}")


@app.get("/completion")
def render_completion_page():
    """Displays completion of survey"""

    return render_template("/completion.html")