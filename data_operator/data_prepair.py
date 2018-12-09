import random
import uuid
import numpy as np
from cached_property import cached_property
from models.consts import VIRTUAL, MOCK_FIRST_NAME, MOCK_SECOND_NAME


class BaseDataInfo(object):
    data_type = VIRTUAL
    student_base_info_list: [{}] = []
    question_base_info_list: [{}] = []


class VirtualBaseData(BaseDataInfo):
    def __init__(self, student_num, exam_length):
        self.student_num = student_num
        self.exam_length = exam_length

    @cached_property
    def virtual_student_info_list(self):
        student_base_info_list = []
        for _ in range(self.student_num):
            student_base_info_list.append(
                {
                    "student_name": (
                        random.choice(MOCK_FIRST_NAME)
                        + random.choice(MOCK_SECOND_NAME)
                        + random.choice(MOCK_SECOND_NAME)
                    ),
                    "student_id": str(uuid.uuid1()),
                    "student_type": VIRTUAL,
                }
            )
        return student_base_info_list

    @cached_property
    def virtual_exam_paper_info_list(self):
        question_base_info_list = []
        for question_index in range(self.exam_length):
            question_base_info_list.append(
                {
                    "question_index": question_index,
                    "question_type": "choice",
                    "question_full_score": 5,
                }
            )
        return question_base_info_list

    @cached_property
    def virtual_exam_paper_info_array(self):
        question_info_list = [
            [
                question["question_index"],
                question["question_type"],
                question["question_full_score"],
            ]
            for question in self.virtual_exam_paper_info_list
        ]
        return np.array(question_info_list)

    @cached_property
    def virtual_exam_people_score_info_array(self):
        name_list = ["student_name"] + [
            student["student_name"] for student in self.virtual_student_info_list
        ]
        id_list = ["student_id"] + [
            student["student_id"] for student in self.virtual_student_info_list
        ]
        question_index_list = [
            question["question_index"]
            for question in self.virtual_exam_paper_info_list
        ]
        score_matrix = np.random.choice([0, 5], (self.student_num, self.exam_length))
        return np.hstack(
            (
                np.array(name_list).reshape(len(name_list), 1),
                np.array(id_list).reshape(len(id_list), 1),
                np.vstack((np.array(question_index_list), score_matrix)),
            )
        )
