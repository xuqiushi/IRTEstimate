from models import VirtualStudentClass, RealStudentClass
from models import VirtualExamPaper, RealExamPaper


class Examination(object):
    def __init__(
        self,
        student_class: VirtualStudentClass or RealStudentClass,
        exam_paper: VirtualExamPaper or RealExamPaper,
    ):
        self.student_class = student_class
        self.exam_paper = exam_paper

        
