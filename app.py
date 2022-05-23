import uuid

from flask import Flask, request, jsonify
from flask import render_template

from form import *

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
forms = {}

@app.route("/")
@app.route("/home/")
def home():
    return render_template("home.html")

@app.route("/user-form/")
@app.route("/user-form/<guid>")
def user_form(guid = None):
    print(guid)
    form = None
    if guid != None and guid in forms:
        form = forms[guid]
        print(guid)
    return render_template("user-form.html", form=form)

@app.route("/edit-form/")
def edit_form():
    return render_template("edit-form.html")

@app.route('/edit-form/post', methods=['GET', 'POST'])
def post_form():
    content = request.get_json()
    
    form = parse_form(json.dumps(content))
    guid = str(uuid.uuid4())
    forms[guid] = form

    return jsonify(guid=guid)