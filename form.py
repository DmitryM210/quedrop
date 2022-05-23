import json

class Question:
    def __init__(self, text, answer=None):
        self.text = text
        self.answer = answer
        self.correct = False

    def mark_correct(self):
        self.correct = True

    def mark_incorrect(self):
        self.correct = False

class Form:
    def __init__(self, title, description, questions):
        self.title = title
        self.description = description
        self.questions = questions
        self.questions_count = len(questions)

class Answer(Form):
    def __init__(self, title, description, questions):
        super().__init__(title, description, questions)
        self.status = "Unchecked"
        self.count_correct_questions()

    def start_checking(self):
        self.status = "Checking"

    def end_checking(self):
        self.status = "Checked"
        self.count_correct_questions()

    def count_correct_questions(self):
        self.correct_question_count = 0
        for question in self.questions:
            if question.correct:
                self.correct_question_count += 1

def parse_form(json_data):
    data = json.loads(json_data)
    
    title = data['title']
    description = data['description']
    questions = []

    for key in data:
        if key != 'title' and key != 'description':
            question = Question(data[key])
            questions.append(question)
    
    return Form(title, description, questions)

def parse_answer(json_data):
    data = json.loads(json_data)
    
    title = data['title']
    description = data['description']
    questions = []

    for key in data:
        if key.startswith("question"):
            question_text = data[key]["question"]
            answer_text = data[key]["answer"]
            question = Question(question_text, answer_text)
            questions.append(question)

    return Answer(title, description, questions)

def check_answers(answer, json_data):
    data = json.loads(json_data)
    
    for question in answer.questions:
        question.mark_incorrect()

    for key in data:
        if key.startswith("is_correct"):
            question_text = data[key]["question"]
            question = next(x for x in answer.questions if x.text == question_text)
            question.mark_correct()
    
    answer.end_checking()