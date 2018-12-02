from consts import MOCK_CLASS_SIZE, MOCK_EXAM_LENGTH
from models import VirtualStudentClass, VirtualExamPaper, Examination


def generate_mock_class(mock_class_size):
    return VirtualStudentClass(mock_class_size)


def generate_mock_exam(mock_exam_length):
    return VirtualExamPaper(mock_exam_length)


if __name__ == "__main__":
    virtual_class = generate_mock_class(MOCK_CLASS_SIZE)
    virtual_exam = generate_mock_exam(MOCK_EXAM_LENGTH)
    examination = Examination(virtual_class, virtual_exam)
