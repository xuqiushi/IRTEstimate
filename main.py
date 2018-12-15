from consts import MOCK_CLASS_SIZE, MOCK_EXAM_LENGTH
from models import ScoreTable, Examination
from data_operator import VirtualBaseData, IRTEstimate

if __name__ == "__main__":

    # 生成mock数据
    test_data_obj = VirtualBaseData(MOCK_CLASS_SIZE, MOCK_EXAM_LENGTH)

    # 生成基础信息
    score_table = ScoreTable(
        test_data_obj.virtual_exam_paper_info_array,
        test_data_obj.virtual_exam_people_score_info_array,
    )

    # 创建本次考试
    examination = Examination(score_table)

    # 筛选一下零分和满分
    examination.update_state_at_first()

    # 估计一下试试
    test_estimate = IRTEstimate(examination.score_array_for_estimate)
    print(test_estimate.question_initial_values)
    print(test_estimate.p_calculate())
    print(test_estimate.ability_jacobi_matrix_calculate)
    print(test_estimate.ability_hessian_matrix_calculate)
    print(test_estimate.difficulty_jacobi_matrix_calculate)
    print(test_estimate.difficulty_hessian_matrix_calculate)
