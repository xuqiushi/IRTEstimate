import numpy as np
from models import StudentClass, ExamPaper, ScoreTable
from cached_property import cached_property


class Examination(object):
    def __init__(
        self,
        student_class: StudentClass,
        exam_paper: ExamPaper,
        score_table: ScoreTable,
    ):
        self.student_class = student_class
        self.exam_paper = exam_paper
        self.score_table = score_table
