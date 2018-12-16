from consts import MOCK_CLASS_SIZE, MOCK_EXAM_LENGTH
from models import ScoreTable, Examination
from data_operator import VirtualBaseData, IRTEstimate
import numpy as np

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
    test_estimate = IRTEstimate(
        examination.score_array_for_estimate,
        np.array(test_data_obj.virtual_student_abilities_list)[examination.effective_student_index],
        np.array(test_data_obj.virtual_question_difficulties_list)[examination.effective_question_index],
    )
    test_estimate.merge_approach()
