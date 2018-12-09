from consts import MOCK_CLASS_SIZE, MOCK_EXAM_LENGTH
from models import ScoreTable, Examination
from data_operator.data_prepair import VirtualBaseData

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

    # test = examination.score_transcript
