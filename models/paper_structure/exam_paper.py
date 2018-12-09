from models import Question


class ExamPaper(object):
    effective_question_index = []

    def __init__(self, question_info_list):
        self.question_list = [
            Question(question[1], question[2])
            for question in question_info_list
        ]
