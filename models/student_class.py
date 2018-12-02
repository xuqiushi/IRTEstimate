from models.consts import VIRTUAL, REAL
from models.student import VirtualStudent


class StudentClass(object):
    class_type = VIRTUAL


class VirtualStudentClass(StudentClass):
    """
    根绝设定班级大小，mock班级
    """
    def __init__(self, class_size: int):
        self.student_list = []
        for index in range(class_size):
            self.student_list.append(VirtualStudent())


class RealStudentClass(StudentClass):
    class_type = REAL

    def __init__(self, student_list: list):
        self.student_list = student_list
