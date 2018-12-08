import random
import uuid
import json
import numpy as np
from numpy import ndarray
from models.consts import (
    VIRTUAL,
    REAL,
    MOCK_FIRST_NAME,
    MOCK_SECOND_NAME,
    STUDENT_FULL_SCORE,
    STUDENT_NORMAL_SCORE,
    STUDENT_ZERO_SCORE,
)
from models.exam_paper import VirtualExamPaper
from models.exceptions import QuestionTypeSupportError


class StudentBase(object):
    student_type: str = VIRTUAL
    effective_score_index: list = []
    ability_of_student: float = 0
    student_score_state: str = STUDENT_NORMAL_SCORE  # 默认分数状态

    def __str__(self) -> str:
        print_dict = {
            "student_type": self.student_type,
            "effective_score_index": self.effective_score_index,
        }
        print_dict.update(self.__dict__)
        for key, value in print_dict.items():
            if isinstance(value, ndarray):
                print_dict[key] = value.tolist()
        return json.dumps(
            print_dict,
            indent=4,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )

    @classmethod
    def update_effective_score_index(cls, effective_score_index: [bool]):
        """
        直接更新类属性，让所有学生保持一致的长度和位置
        """
        cls.effective_score_index = effective_score_index


class VirtualStudent(StudentBase):
    """
    mock学生，基本上毛线也不用传，直接初始化
    """

    def __init__(self):
        self.name: str = (
            random.choice(MOCK_FIRST_NAME)
            + random.choice(MOCK_SECOND_NAME)
            + random.choice(MOCK_SECOND_NAME)
        )
        self.student_id: str = str(uuid.uuid1())
        self.score_list: ndarray = np.array([])
        self.effective_score_index: list = []
        self.student_score_state = self.student_score_state

    def update_score_list(self, exam_paper: VirtualExamPaper):
        """
        录入本次考试的成绩
        """
        self.score_list = np.zeros(len(exam_paper.question_list))
        for question_index, question in enumerate(exam_paper.question_list):
            if question.question_type is not "choice":
                raise QuestionTypeSupportError("仅支持选择题")
            self.score_list[question_index] = self._random_score_generator(
                question.question_type, question.question_full_score
            )
        self._update_student_state(exam_paper.full_score_list)

    def _update_student_state(self, full_score_list):
        if (self.score_list == full_score_list).all():
            self.student_score_state = STUDENT_FULL_SCORE
        elif (self.score_list == 0).all():
            self.student_score_state = STUDENT_ZERO_SCORE

    @classmethod
    def _random_score_generator(cls, question_type, full_score):
        # 仅支持选择题
        if question_type is "choice":
            return random.choice([0, full_score])


class RealStudent(StudentBase):
    student_type = REAL

    def __init__(self, name: str, student_id: str, score_list: list):
        self.name = name
        self.student_id = student_id
        self.score_list = score_list
