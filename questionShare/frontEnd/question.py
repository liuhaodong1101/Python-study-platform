class Question:
    def __init__(self, question_name, question_group):
        self.question_name = question_name
        self.question_group = question_group


class EssayQuestion(Question):
    def __init__(self, question_name, question_answer, question_group):
        super().__init__(question_name, question_group)
        self.question_answer = question_answer


class MultipleChoiceQuestion(Question):
    def __init__(self, question_name, options, question_group):
        super().__init__(question_name, question_group)
        self.options = options
