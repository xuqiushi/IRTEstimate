import numpy as np
from cached_property import cached_property


class IRTEstimate(object):
    """
    将所有题目按照选择题处理
    """

    def __init__(self, score_array):
        self.score_array = score_array
        self.score_array[self.score_array > 0] = 1

    @cached_property
    def student_initial_values(self):
        student_right_count_list = np.sum(self.score_array, axis=1)
        student_wrong_count_list = (
            np.sum(
                np.ones((self.score_array.shape[0], self.score_array.shape[1])), axis=1
            )
            - student_right_count_list
        )
        return np.log(student_right_count_list / student_wrong_count_list)

    @cached_property
    def question_initial_values(self):
        question_right_count_list = np.sum(self.score_array, axis=0)
        question_wrong_count_list = (
            np.sum(
                np.ones((self.score_array.shape[0], self.score_array.shape[1])), axis=0
            )
            - question_right_count_list
        )
        return np.log(question_wrong_count_list / question_right_count_list)
