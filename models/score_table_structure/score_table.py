from cached_property import cached_property
import numpy as np


class ScoreTable(object):
    student_id_list = []
    student_score_list = []
    exam_question_index = []
    exam_full_score_list = []

    def __init__(self, base_question_info, base_score_array):
        self.base_score_array = base_score_array
        self.base_question_info = base_question_info

    @cached_property
    def student_info_list(self):
        return [
            student_info
            for student_info in self.base_score_array[
                1:, np.isin(self.base_score_array[0, :], ["student_name", "student_id"])
            ]
        ]

    @cached_property
    def question_info_list(self):
        return [question_info for question_info in self.base_question_info]

    @cached_property
    def score_info_array(self):
        return self.base_score_array[1:, 2:]
