from flask import Flask
from flask import render_template

from form import *

app = Flask(__name__)

questions = [ Question("quest1"), Question("quest2") ]
form = Form("Opros1", "desc1", questions)

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/user-form")
def user_form():
    return render_template("user-form.html", form=form)

@app.route("/edit-form")
def edit_form():
    return render_template("edit-form.html", form=form)