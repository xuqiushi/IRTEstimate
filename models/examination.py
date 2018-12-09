from models import StudentClass, ExamPaper, ScoreTable
import numpy as np


class Examination(object):
    def __init__(self, base_score_table: ScoreTable):
        self.base_score_table = base_score_table
        self.student_class = StudentClass(self.base_score_table.student_info_list)
        self.exam_paper = ExamPaper(self.base_score_table.question_info_list)
        self.base_score_array = self.base_score_table.score_info_array.astype(np.int)
        self.effective_student_index = []
        self.effective_question_index = []
        self.score_array_for_estimate = []

    def update_state_at_first(self):
        jude_satisfied_var = False
        score_array_temp = self.base_score_array
        effective_question_index_temp = np.array(
            [True] * len(self.base_score_table.question_info_list)
        )
        effective_student_index_temp = np.array(
            [True] * len(self.base_score_table.student_info_list)
        )

        while not jude_satisfied_var:
            full_paper_score_for_student = np.sum(
                self.exam_paper.full_score_list[effective_question_index_temp]
            )
            full_paper_score_list_for_question = (
                self.exam_paper.full_score_list[effective_question_index_temp]
                * score_array_temp[effective_student_index_temp, :].shape[0]
            )
            jude_satisfied_var, sub_effective_student_index, sub_effective_question_index = self._judge_satisfied_array(
                self.base_score_array[
                    np.ix_(effective_student_index_temp, effective_question_index_temp)
                ],
                full_paper_score_for_student,
                full_paper_score_list_for_question,
            )
            effective_question_index_temp[
                effective_question_index_temp
            ] = sub_effective_question_index
            effective_student_index_temp[
                effective_student_index_temp
            ] = sub_effective_student_index
        self.effective_student_index = effective_student_index_temp
        self.effective_question_index = effective_question_index_temp
        self.score_array_for_estimate = self.base_score_array[
            np.ix_(self.effective_student_index, self.effective_question_index)
        ]

    @classmethod
    def _judge_satisfied_array(
        cls,
        score_array,
        full_paper_score_for_student,
        full_paper_score_list_for_question,
    ):
        update_student_list = [True] * score_array.shape[0]
        update_question_list = [True] * score_array.shape[1]
        is_satisfied = True
        student_not_satisfied_index = np.logical_or(
            np.sum(score_array, axis=1) == full_paper_score_for_student,
            np.sum(score_array, axis=1) == 0,
        )
        if student_not_satisfied_index.any():
            is_satisfied = False
            update_student_list = ~student_not_satisfied_index
        question_not_satisfied_index = np.logical_or(
            np.sum(score_array, axis=0) == full_paper_score_list_for_question,
            np.sum(score_array, axis=0) == 0,
        )
        if question_not_satisfied_index.any():
            is_satisfied = False
            update_question_list = ~question_not_satisfied_index

        return is_satisfied, update_student_list, update_question_list
