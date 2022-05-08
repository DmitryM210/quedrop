import json

class Question:
    def __init__(self, text):
        self.text = text
        self.answer = None

    def get_text(self):
        return self.text

    def set_answer(self):
        return self.answer

    def set_answer(self, answer_text):
        if self.answer != None:
            raise NotImplementedError('question cannot be answered more than once')
        self.answer = answer_text

class Form:
    def __init__(self, title, description, questions):
        self.title = title
        self.description = description
        self.questions = questions
        self.questions_count = len(questions)

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_questions(self):
        return self.questions

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