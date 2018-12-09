from models import StudentClass, ExamPaper, ScoreTable
import numpy as np


class Examination(object):
    def __init__(
        self,
        base_score_table: ScoreTable,
    ):
        self.base_score_table = base_score_table
        self.student_class = StudentClass(self.base_score_table.student_info_list)
        self.exam_paper = ExamPaper(self.base_score_table.question_info_list)
        self.score_array = self.base_score_table.score_info_array.astype(np.int)
