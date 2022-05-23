import uuid
from flask import Flask, request, jsonify
from flask import render_template
from form import *

app = Flask(__name__)
guids, forms, answers_dict = {}, {}, {}

@app.route("/")
@app.route("/home/")
def home():
    return render_template("home.html")

@app.route("/edit-form/")
def edit_form():
    return render_template("edit-form.html")

@app.route("/user-form/")
@app.route("/user-form/<public_guid>")
def user_form(public_guid = None):
    form = None
    if public_guid != None and public_guid in forms:
        form = forms[public_guid]
    return render_template("user-form.html", form=form)

@app.route("/user-answer/<private_guid>/<index>")
def user_answer(private_guid, index):
    answer = answers_dict[private_guid][int(index)]
    return render_template("user-answer.html", answer=answer)

@app.route("/form-list/<private_guid>")
def form_list(private_guid = None):
    answers = None
    if private_guid != None and private_guid in answers_dict:
        answers = answers_dict[private_guid]
    return render_template("form-list.html", 
        answers=answers, private_guid=private_guid)

@app.route('/edit-form/post', methods=['GET', 'POST'])
def post_form():
    content = request.get_json()
    form = parse_form(json.dumps(content))

    private_guid = str(uuid.uuid4())
    public_guid = str(uuid.uuid4())
    guids[public_guid] = private_guid
    guids[private_guid] = public_guid # todo: mb remove?
    forms[public_guid] = form
    answers_dict[private_guid] = []

    return jsonify(
        public_guid=public_guid, 
        private_guid=private_guid
        )

@app.route('/user-form/post', methods=['GET', 'POST'])
def post_answer():
    content = request.get_json()

    public_guid = content["public_guid"]
    private_guid = guids[public_guid]
    answer = parse_answer(json.dumps(content))
    
    answers_dict[private_guid].append(answer)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}