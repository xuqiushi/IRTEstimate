from models import Question


class ExamPaper(object):
    effective_question_index = []

    def __init__(self, question_info_list):
        self.question_list = [
            Question(info["question_type"], info["question_full_score"])
            for info in question_info_list
        ]
