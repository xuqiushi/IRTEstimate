from models import Student


class StudentClass(object):
    def __init__(self, student_base_info: dict):
        self.student_list = [
            Student(
                base_info[0],
                base_info[1],
            )
            for base_info in student_base_info
        ]
