from urllib import response
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
RESPONSES = []

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

    return redirect("/question/0")


@app.get("/question/<int:index>")
def render_question(index):
    """Displays current question and input"""

    if len(RESPONSES) == len(survey.questions):
        return redirect("/completion")
    else:
        question = survey.questions[index]
        return render_template("question.html", question=question)


@app.post("/answer")
def redirect_answer():
    """Redirect to next question store answer in RESPONSES"""

    RESPONSES.append(request.form["answer"])
    next_question = len(RESPONSES)
    return redirect(F"/question/{next_question}")


@app.get("/completion")
def render_completion_page():
    """Displays completion of survey"""
    
    # print(RESPONSES)
    return render_template("/completion.html")