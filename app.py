from urllib import response
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"

@app.get("/")
def render_survey_start():
    """Displays survey title and start on the page"""

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