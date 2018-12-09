from models import Question
from cached_property import cached_property
import numpy as np


class ExamPaper(object):
    effective_question_index = []

    def __init__(self, question_info_list):
        self.question_list = [
            Question(question[1], question[2])
            for question in question_info_list
        ]

    @cached_property
    def full_score_list(self):
        return np.array([question.question_full_score for question in self.question_list]).astype(np.int)
