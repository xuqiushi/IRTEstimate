import json
import numpy as np
from numpy import ndarray
from models.consts import (
    STUDENT_FULL_SCORE,
    STUDENT_NORMAL_SCORE,
    STUDENT_ZERO_SCORE,
)


class Student(object):

    score_list: np.ndarray = []
    effective_score_index: list = []
    ability_of_student: float = 0
    student_score_state: str = STUDENT_NORMAL_SCORE  # 默认分数状态

    def __init__(self, student_name, student_id, student_type):
        self.student_name = student_name
        self.student_id = student_id
        self.student_type: str = student_type

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

    def _update_student_state(self, full_score_list):
        if (self.score_list == full_score_list).all():
            self.student_score_state = STUDENT_FULL_SCORE
        elif (self.score_list == 0).all():
            self.student_score_state = STUDENT_ZERO_SCORE
