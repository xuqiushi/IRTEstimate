from models.consts import CHOICE, VIRTUAL, REAL


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


class VirtualExamPaper(ExamPaperBase):
    """
    根据指定题目数量，生成一定量的满分为5的选择题作为模拟数据
    """

    def __init__(self, exam_length: int):
        self.question_list = []
        for _ in range(exam_length):
            self.question_list.append(Question(CHOICE, 5))


class RealExamPaper(ExamPaperBase):
    exam_type = REAL

    def __init__(self, question_list):
        self.question_list = question_list
