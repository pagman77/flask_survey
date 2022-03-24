from urllib import response
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


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

    session["responses"] = []
    return redirect("/question/0")


@app.get("/question/<int:next_question>")
def render_question(next_question):
    """Displays current question and input"""

    responses_length = len(session["responses"])

    if responses_length != next_question:
        flash("Please answer a valid question")
        return redirect(f"/question/{responses_length}")

    if responses_length == len(survey.questions):
        return redirect("/completion")
    else:
        question = survey.questions[next_question]
        return render_template("question.html", question=question)


@app.post("/answer")
def redirect_answer():
    """Redirect to next question store answer in RESPONSES"""

    response = session["responses"]
    response.append(request.form["answer"])
    session["responses"] = response

    next_question = len(response)
    return redirect(F"/question/{next_question}")


@app.get("/completion")
def render_completion_page():
    """Displays completion of survey"""

    return render_template("/completion.html")