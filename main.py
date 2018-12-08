from consts import MOCK_CLASS_SIZE, MOCK_EXAM_LENGTH
from models import StudentClass, ExamPaper, ScoreTable, Examination
from data_operator.data_prepair import VirtualBaseData

if __name__ == "__main__":

    # 生成mock数据
    test_data_obj = VirtualBaseData(MOCK_CLASS_SIZE, MOCK_EXAM_LENGTH)

    # 生成班级

    student_class = StudentClass(test_data_obj.virtual_student_info_list)

    # 生成试卷

    exam_paper = ExamPaper(test_data_obj.virtual_exam_paper_info_list)

    # 生成成绩信息

    score_table = ScoreTable(test_data_obj.virtual_exam_paper_info_array)

    # 创建本次考试
    examination = Examination(student_class, exam_paper, score_table)

    # test = examination.score_transcript
