import numpy as np
from cached_property import cached_property
from data_operator.consts import (
    D,
    P_AVERAGE_THETA,
    ABILITY_THETA,
    DIFFICULTY_THETA,
    MAX_EDGE,
    MIN_EDGE,
    MAX_COUNTER,
)

try:
    import matplotlib.pyplot as plt
except ImportError:
    print(
        "Can't import plt."
        "\nYou can go to:\n"
        "'https://markhneedham.com/blog/2018/05/04/python-runtime-error-osx-matplotlib-not-installed-as-framework-mac/'"
        "\n or use merge_approach"
    )
    raise ValueError("plt 引入错误")
import matplotlib


class IRTEstimate(object):
    """
    将所有题目按照选择题处理
    """

    def __init__(self, score_array, target_abilities=None, target_difficulties=None):
        self.score_array = score_array
        self.score_array[self.score_array > 0] = 1
        self.student_abilities = self.student_initial_values
        self.question_difficulties = self.question_initial_values
        self.target_abilities = target_abilities
        self.target_difficulties = target_difficulties

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

    def generate_student_abilities_matrix(self, updated_abilities=np.array([False])):
        if updated_abilities.any():
            return np.tile(
                updated_abilities, (self.question_difficulties.shape[0], 1)
            ).T
        else:
            return np.tile(
                self.student_abilities, (self.question_difficulties.shape[0], 1)
            ).T

    def generate_question_difficulties_matrix(
        self, updated_difficulties=np.array([False])
    ):
        if updated_difficulties.any():
            return np.tile(updated_difficulties, (self.student_abilities.shape[0], 1))
        else:
            return np.tile(
                self.question_difficulties, (self.student_abilities.shape[0], 1)
            )

    @cached_property
    def e_matrix(self):
        return (
            np.ones(
                (self.student_abilities.shape[0], self.question_difficulties.shape[0])
            )
            * np.e
        )

    def p_calculate(
        self,
        updated_abilities=np.array([False]),
        updated_difficulties=np.array([False]),
    ):
        student_abilities_matrix = self.generate_student_abilities_matrix(
            updated_abilities=updated_abilities
        )
        question_difficulties_matrix = self.generate_question_difficulties_matrix(
            updated_difficulties=updated_difficulties
        )
        log_p = self.score_array * (
            np.log(
                1
                / (
                    1
                    + np.power(
                        self.e_matrix,
                        -D * (student_abilities_matrix - question_difficulties_matrix),
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
                        -D * (student_abilities_matrix - question_difficulties_matrix),
                    )
                )
            )
        )
        return np.sum(log_p)

    def ability_jacobi_matrix_calculate(self, updated_abilities=np.array([False])):
        return np.matrix(
            np.sum(
                self._jacobi_matrix_calculate(updated_abilities=updated_abilities),
                axis=1,
            )
        ).T

    def ability_hessian_matrix_calculate(self, updated_abilities=np.array([False])):
        return np.matrix(
            np.diag(
                np.sum(
                    self._hessian_matrix_calculate(updated_abilities=updated_abilities),
                    axis=1,
                )
            )
        )

    def difficulty_jacobi_matrix_calculate(
        self, updated_difficulties=np.array([False])
    ):
        return np.matrix(
            np.sum(
                -self._jacobi_matrix_calculate(
                    updated_difficulties=updated_difficulties
                ),
                axis=0,
            )
        ).T

    def difficulty_hessian_matrix_calculate(
        self, updated_difficulties=np.array([False])
    ):
        return np.matrix(
            np.diag(
                np.sum(
                    -self._hessian_matrix_calculate(
                        updated_difficulties=updated_difficulties
                    ),
                    axis=0,
                )
            )
        )

    def _jacobi_matrix_calculate(
        self,
        updated_abilities=np.array([False]),
        updated_difficulties=np.array([False]),
    ):
        student_abilities_matrix = self.generate_student_abilities_matrix(
            updated_abilities=updated_abilities
        )
        question_difficulties_matrix = self.generate_question_difficulties_matrix(
            updated_difficulties=updated_difficulties
        )
        jacobi_calculate_matrix = self.score_array * D / (
            1
            + np.power(
                self.e_matrix,
                D * (student_abilities_matrix - question_difficulties_matrix),
            )
        ) + (1 - self.score_array) * (-D) / (
            1
            + np.power(
                self.e_matrix,
                (-D) * (student_abilities_matrix - question_difficulties_matrix),
            )
        )
        return jacobi_calculate_matrix

    def _hessian_matrix_calculate(
        self,
        updated_abilities=np.array([False]),
        updated_difficulties=np.array([False]),
    ):
        student_abilities_matrix = self.generate_student_abilities_matrix(
            updated_abilities=updated_abilities
        )
        question_difficulties_matrix = self.generate_question_difficulties_matrix(
            updated_difficulties=updated_difficulties
        )
        hessian_calculate_matrix = -np.power(D, 2) * self.score_array * (
            np.power(
                self.e_matrix,
                D * (student_abilities_matrix - question_difficulties_matrix),
            )
        ) / np.power(
            1
            + np.power(
                self.e_matrix,
                D * (student_abilities_matrix - question_difficulties_matrix),
            ),
            2,
        ) - np.power(
            D, 2
        ) * (
            1 - self.score_array
        ) * (
            np.power(
                self.e_matrix,
                (-D) * (student_abilities_matrix - question_difficulties_matrix),
            )
        ) / np.power(
            1
            + np.power(
                self.e_matrix,
                (-D) * (student_abilities_matrix - question_difficulties_matrix),
            ),
            2,
        )
        return hessian_calculate_matrix

    def ability_approach(self):
        max_edge = MAX_EDGE
        min_edge = MIN_EDGE
        decline_direction = self.ability_hessian_matrix_calculate().I
        while (
            np.sum(np.power(self.ability_jacobi_matrix_calculate(), 2)) > ABILITY_THETA
        ):
            decline_size = -decline_direction * self.ability_jacobi_matrix_calculate()
            while max_edge - min_edge > 0.01:
                min_edge_attempt = min_edge + 0.382 * (max_edge - min_edge)
                max_edge_attempt = min_edge + 0.618 * (max_edge - min_edge)
                up_updated_abilities = self.ability_jacobi_matrix_calculate(
                    self.student_abilities
                    - (
                        min_edge_attempt
                        * decline_direction
                        * self.ability_jacobi_matrix_calculate()
                    ).reshape(self.student_abilities.shape[0])
                )
                down_updated_abilities = self.ability_jacobi_matrix_calculate(
                    self.student_abilities
                    - (
                        max_edge_attempt
                        * decline_direction
                        * self.ability_jacobi_matrix_calculate()
                    ).reshape(self.student_abilities.shape[0])
                )
                if np.sqrt(np.sum(np.power(up_updated_abilities, 2))) > np.sqrt(
                    np.sum(np.power(down_updated_abilities, 2))
                ):
                    min_edge = min_edge_attempt
                else:
                    max_edge = max_edge_attempt
            average_edge = (max_edge + min_edge) / 2
            # average_edge = 0.0001
            updated_decline_size = average_edge * decline_size
            updated_student_abilities = (
                self.student_abilities
                + updated_decline_size.reshape(self.student_abilities.shape[0])
            )
            abilities_difference = (
                self.ability_jacobi_matrix_calculate(
                    np.array(updated_student_abilities).flatten()
                )
                - self.ability_jacobi_matrix_calculate()
            )

            decline_direction = (
                (
                    np.matrix(np.eye(self.student_abilities.shape[0]))
                    - (updated_decline_size * abilities_difference.T)
                    / (abilities_difference.T * updated_decline_size)
                )
                * decline_direction
                * (
                    np.matrix(np.eye(self.student_abilities.shape[0]))
                    - (abilities_difference * updated_decline_size.T)
                    / (abilities_difference.T * updated_decline_size)
                )
            ) + (updated_decline_size * updated_decline_size.T) / (
                abilities_difference.T * updated_decline_size
            )
            self.student_abilities = np.array(updated_student_abilities).flatten()

    def difficulty_approach(self):
        max_edge = MAX_EDGE
        min_edge = MIN_EDGE
        decline_direction = self.difficulty_hessian_matrix_calculate().I
        while (
            np.power(np.sum(self.difficulty_jacobi_matrix_calculate()), 2)
            > DIFFICULTY_THETA
        ):
            decline_size = (
                -decline_direction * self.difficulty_jacobi_matrix_calculate()
            )
            while max_edge - min_edge > 0.01:
                min_edge_attempt = min_edge + 0.382 * (max_edge - min_edge)
                max_edge_attempt = min_edge + 0.618 * (max_edge - min_edge)
                up_updated_difficulties = self.difficulty_jacobi_matrix_calculate(
                    self.question_difficulties
                    - (
                        min_edge_attempt
                        * decline_direction
                        * self.difficulty_jacobi_matrix_calculate()
                    ).reshape(self.question_difficulties.shape[0])
                )
                down_updated_difficulties = self.difficulty_jacobi_matrix_calculate(
                    self.question_difficulties
                    - (
                        min_edge_attempt
                        * decline_direction
                        * self.difficulty_jacobi_matrix_calculate()
                    ).reshape(self.question_difficulties.shape[0])
                )
                if np.sqrt(np.sum(np.power(up_updated_difficulties, 2))) > np.sqrt(
                    np.sum(np.power(down_updated_difficulties, 2))
                ):
                    min_edge = min_edge_attempt
                else:
                    max_edge = max_edge_attempt
            average_edge = (max_edge + min_edge) / 2
            updated_decline_size = average_edge * decline_size
            updated_question_difficulties = (
                self.question_difficulties
                + updated_decline_size.reshape(self.question_difficulties.shape[0])
            )
            difficulties_difference = (
                self.difficulty_jacobi_matrix_calculate(
                    np.array(updated_question_difficulties).flatten()
                )
                - self.difficulty_jacobi_matrix_calculate()
            )

            decline_direction = (
                (
                    np.matrix(np.eye(self.question_difficulties.shape[0]))
                    - (updated_decline_size * difficulties_difference.T)
                    / (difficulties_difference.T * updated_decline_size)
                )
                * decline_direction
                * (
                    np.matrix(np.eye(self.question_difficulties.shape[0]))
                    - (difficulties_difference * updated_decline_size.T)
                    / (difficulties_difference.T * updated_decline_size)
                )
            ) + (updated_decline_size * updated_decline_size.T) / (
                difficulties_difference.T * updated_decline_size
            )
            self.question_difficulties = np.array(
                updated_question_difficulties
            ).flatten()

    def merge_approach(self):
        counter = 0
        print("开始")
        while (
            np.power(np.e, self.p_calculate())
            < np.power(
                P_AVERAGE_THETA,
                self.student_abilities.shape[0] * self.question_difficulties.shape[0],
            )
        ) and counter < MAX_COUNTER:
            difficulties_difference = np.sum(
                self.target_difficulties - self.question_difficulties
            )
            abilities_difference = np.sum(
                self.target_abilities - self.student_abilities
            )
            print(f"当前迭代次数:{counter};当前对数似然函数值:{self.p_calculate()}")
            print(
                f"难度目标值与当前差值之和{difficulties_difference};能力目标与当前差值之和{abilities_difference}"
            )
            self.ability_approach()
            self.difficulty_approach()
            counter += 1

    def merge_approach_graph(self):
        """
        暂时有bug，别用这玩意。用了你电脑死了。
        :return:
        """
        counter = 0
        while (
            np.power(np.e, self.p_calculate())
            < np.power(
                P_AVERAGE_THETA,
                self.student_abilities.shape[0] * self.question_difficulties.shape[0],
            )
        ) and counter < MAX_COUNTER:
            self.ability_approach()
            self.difficulty_approach()
            counter += counter
            plt.ion()
            question_label_list = range(self.question_difficulties.shape[0])
            question_target_list = np.around(self.target_difficulties, 1)
            question_now_list = np.around(self.question_difficulties, 1)
            left_bar_x_position = range(self.target_difficulties.shape[0])
            question_target_bar = plt.bar(
                x=left_bar_x_position,
                height=question_target_list,
                width=0.4,
                alpha=0.8,
                color="red",
                label="目标",
            )
            question_now_bar = plt.bar(
                x=[i + 0.4 for i in left_bar_x_position],
                height=question_now_list,
                width=0.4,
                color="blue",
                label="现在",
            )
            plt.ylim(-3.5, 3.5)
            plt.ylabel("value")
            plt.xticks(
                [index + 0.2 for index in left_bar_x_position], question_label_list
            )
            plt.xlabel("question_index")
            plt.title("question_difficulties_approach")
            plt.legend()
            for bar in question_target_bar:
                height = bar.get_height()
                plt.text(
                    bar.get_x() + bar.get_width() / 2,
                    height + 0.2,
                    str(height),
                    ha="center",
                    va="bottom",
                )
            for bar in question_now_bar:
                height = bar.get_height()
                plt.text(
                    bar.get_x() + bar.get_width() / 2,
                    height + 0.2,
                    str(height),
                    ha="center",
                    va="bottom",
                )
            plt.show()
