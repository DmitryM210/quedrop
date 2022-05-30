import uuid
from flask import Flask, request, make_response, jsonify
from flask import render_template
from form import *

CHECKING_COOKIE_NAME = "checking-session-token"
CHECKING_COOKIE_AGE = 60*60

app = Flask(__name__)
guids, forms, answers_dict = {}, {}, {}
checking_sessions = {}

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

@app.route("/user-answer/<private_guid>/<int:index>")
def user_answer(private_guid, index):
    checking_session_token = request.cookies.get(CHECKING_COOKIE_NAME)
    if private_guid not in answers_dict:
        return render_template("user-answer.html", answer=None, has_permission=False)
    answer = answers_dict[private_guid][index]
    if answer.status == "Unchecked" and checking_session_token not in checking_sessions:
        checking_sessions[checking_session_token] = index
        answer.start_checking()
    if (checking_session_token in checking_sessions and 
        index == checking_sessions[checking_session_token]):
        return render_template("user-answer.html", answer=answer, has_permission=True)
    else:
        return render_template("user-answer.html", answer=answer, has_permission=False)

@app.route("/form-list/<private_guid>")
def form_list(private_guid = None):
    answers = None
    if private_guid != None and private_guid in answers_dict:
        answers = answers_dict[private_guid]
    response = make_response(render_template("form-list.html", 
        answers=answers, private_guid=private_guid))
    checking_session_token = request.cookies.get(CHECKING_COOKIE_NAME)
    if checking_session_token is None:
        token = str(uuid.uuid4())
        response.set_cookie(CHECKING_COOKIE_NAME, token, max_age=CHECKING_COOKIE_AGE)
    return response

@app.route('/edit-form/post', methods=['GET', 'POST'])
def post_form():
    content = request.get_json()
    form = parse_form(json.dumps(content))

    private_guid = str(uuid.uuid4())
    public_guid = str(uuid.uuid4())
    guids[public_guid] = private_guid
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

@app.route('/user-answer/<private_guid>/<index>/post', methods=['GET', 'POST'])
def post_check(private_guid, index):
    content = request.get_json()
    answer = answers_dict[private_guid][int(index)]
    if (answer.status == "Checking"):
        check_answers(answer, json.dumps(content))
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    else:
        return json.dumps({'success':False, 'message':'Already checked'}), 409, {'ContentType':'application/json'}