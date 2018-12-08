from consts import MOCK_CLASS_SIZE, MOCK_EXAM_LENGTH
from models import VirtualStudentClass, VirtualExamPaper, Examination


def generate_mock_class(mock_class_size):
    return VirtualStudentClass(mock_class_size)


def generate_mock_exam(mock_exam_length):
    return VirtualExamPaper(mock_exam_length)


def input_student_score(exist_virtual_class: VirtualStudentClass, exam_paper: VirtualExamPaper):
    for student in exist_virtual_class.student_list:
        student.update_score_list(exam_paper)


if __name__ == "__main__":
    # 创建班级
    virtual_class = generate_mock_class(MOCK_CLASS_SIZE)
    # 创建考试试卷
    virtual_exam = generate_mock_exam(MOCK_EXAM_LENGTH)
    # 录入成绩
    input_student_score(virtual_class, virtual_exam)
    # 创建本次考试
    examination = Examination(virtual_class, virtual_exam)

    test = examination.score_transcript
