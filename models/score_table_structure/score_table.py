class ScoreTable(object):
    student_id_list = []
    student_score_list = []
    exam_question_index = []
    exam_full_score_list = []

    def __init__(self, score_array):
        self.score_array = score_array
