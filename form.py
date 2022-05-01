class Question:
    def __init__(self, text):
        self.text = text
        self.answer = None

    def get_text(self):
        return self.text

    def set_answer(self):
        return self.answer

    def set_answer(self, answer_text):
        if answer != None:
            raise NotImplementedError('question cannot be answered more than once')
        self.answer = answer_text

class Form:
    def __init__(self, title, description, questions):
        self.title = title
        self.description = description
        self.questions = questions

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_questions(self):
        return self.questions