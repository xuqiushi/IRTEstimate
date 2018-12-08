import random
import uuid
import numpy as np
from models.consts import VIRTUAL, MOCK_FIRST_NAME, MOCK_SECOND_NAME


class BaseDataInfo(object):
    data_type = VIRTUAL
    student_base_info_list: [{}] = []
    question_base_info_list: [{}] = []

    @classmethod
    def _random_score_generator(cls, question_type, full_score):
        # 仅支持选择题
        if question_type is "choice":
            return random.choice([0, full_score])


class VirtualBaseData(BaseDataInfo):

    def __init__(self, student_num, exam_length):
        self.student_num = student_num
        self.exam_length = exam_length

    @property
    def virtual_student_info_list(self):
        student_base_info_list = []
        for _ in range(self.student_num):
            student_base_info_list.append({
                "student_name": (
                    random.choice(MOCK_FIRST_NAME)
                    + random.choice(MOCK_SECOND_NAME)
                    + random.choice(MOCK_SECOND_NAME)
                ),
                "student_id": str(uuid.uuid1()),
                "student_type": VIRTUAL,
            })
        return student_base_info_list

    @property
    def virtual_exam_paper_info_list(self):
        question_base_info_list = []
        for _ in range(self.exam_length):
            question_base_info_list.append(
                {
                    "question_type": 'choice',
                    "question_full_score": 5,
                }
            )
        return question_base_info_list

    @property
    def virtual_exam_paper_info_array(self):
        return np.random.choice([0, 5], (self.student_num, self.exam_length))
