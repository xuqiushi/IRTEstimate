import numpy as np
from cached_property import cached_property
from data_operator.consts import D


class IRTEstimate(object):
    """
    将所有题目按照选择题处理
    """

    def __init__(self, score_array):
        self.score_array = score_array
        self.score_array[self.score_array > 0] = 1
        self.student_abilities = self.student_initial_values
        self.question_difficulties = self.question_initial_values

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

    @property
    def student_abilities_matrix(self):
        return np.tile(
            self.student_abilities, (self.question_difficulties.shape[0], 1)
        ).T

    @property
    def question_difficulties_matrix(self):
        return np.tile(self.question_difficulties, (self.student_abilities.shape[0], 1))

    @cached_property
    def e_matrix(self):
        return (
            np.ones(
                (self.student_abilities.shape[0], self.question_difficulties.shape[0])
            )
            * np.e
        )

    def p_calculate(self):
        log_p = self.score_array * (
            np.log(
                1
                / (
                    1
                    + np.power(
                        self.e_matrix,
                        -D
                        * (
                            self.student_abilities_matrix
                            - self.question_difficulties_matrix
                        ),
                    )
                )
            )
        ) + (1 - self.score_array) * (
            np.log(
                1
                - 1
                / (
                    1
                    + np.power(
                        self.e_matrix,
                        -D
                        * (
                            self.student_abilities_matrix
                            - self.question_difficulties_matrix
                        ),
                    )
                )
            )
        )
        return np.sum(log_p)

    def ability_jacobi_matrix_calculate(self):
        jacobi_calculate_matrix = self.score_array / (
            1
            + np.power(
                self.e_matrix,
                D * (self.student_abilities_matrix - self.question_difficulties_matrix),
            )
        ) + (1 - self.score_array) * (-D) / (
            1
            + np.power(
                self.e_matrix,
                (-D)
                * (self.student_abilities_matrix - self.question_difficulties_matrix),
            )
        )
        return np.sum(jacobi_calculate_matrix, axis=1)

    def ability_hessian_matrix_calculate(self):
        pass

    def difficulty_jacobi_matrix_calculate(self):
        pass

    def difficulty_hessian_matrix_calculate(self):
        pass
