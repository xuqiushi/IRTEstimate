import numpy as np
from models import VirtualStudentClass, RealStudentClass
from models import VirtualExamPaper, RealExamPaper
from cached_property import cached_property


class Examination(object):
    def __init__(
        self,
        student_class: VirtualStudentClass or RealStudentClass,
        exam_paper: VirtualExamPaper or RealExamPaper,
    ):
        self.student_class = student_class
        self.exam_paper = exam_paper

    @cached_property
    def score_transcript(self):
        return np.vstack(
            (student.score_list for student in self.student_class.student_list)
        )
