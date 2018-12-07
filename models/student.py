import random
import uuid
import json
import numpy as np
from numpy import ndarray
from models.consts import VIRTUAL, REAL, MOCK_FIRST_NAME, MOCK_SECOND_NAME


class StudentBase(object):
    student_type: str = VIRTUAL
    effective_score_index: list = []
    ability_of_student: float = 0

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

    def update_score_list(self, question_quantity):
        """
        录入本次考试的成绩
        """
        self.score_list = np.random.randint(0, 2, size=(1, question_quantity))


class RealStudent(StudentBase):
    student_type = REAL

    def __init__(self, name: str, student_id: str, score_list: list):
        self.name = name
        self.student_id = student_id
        self.score_list = score_list
