import json

class Question:
    def __init__(self, text, answer=None):
        self.text = text
        self.answer = answer

class Form:
    def __init__(self, title, description, questions):
        self.title = title
        self.description = description
        self.questions = questions
        self.questions_count = len(questions)

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

    return Form(title, description, questions)