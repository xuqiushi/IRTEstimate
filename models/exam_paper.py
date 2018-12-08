import numpy as np
from models.consts import CHOICE, VIRTUAL, REAL
from cached_property import cached_property


class Question(object):
    def __init__(
        self,
        question_type: str,
        question_full_score: int,
        difficulty_of_question: float = 0,
    ):
        self.question_type = question_type
        self.question_full_score = question_full_score
        self.difficulty_of_question = difficulty_of_question


class ExamPaperBase(object):
    exam_type = VIRTUAL
    effective_question_index = []
    question_list = []

    def add_questions(self, question: Question):
        self.question_list.append(question)

    @cached_property
    def full_score_list(self):
        return np.array([question.question_full_score for question in self.question_list])


class VirtualExamPaper(ExamPaperBase):
    """
    根据指定题目数量，生成一定量的满分为5的选择题作为模拟数据
    """

    def __init__(self, exam_length: int):
        self.question_list = []
        for _ in range(exam_length):
            self.add_questions(Question(CHOICE, 5))


class RealExamPaper(ExamPaperBase):
    exam_type = REAL

    def __init__(self, question_list):
        self.question_list = question_list
