from models import Student


class StudentClass(object):
    def __init__(self, student_base_info: dict):
        self.student_list = [
            Student(
                base_info["student_name"],
                base_info["student_id"],
                base_info["student_type"],
            )
            for base_info in student_base_info
        ]
