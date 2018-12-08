from models.consts import QUESTION_NORMAL_SCORE


class Question(object):
    def __init__(
        self,
        question_type: str,
        question_full_score: int,
        difficulty_of_question: float = 0,
        question_score_state: str = QUESTION_NORMAL_SCORE,
    ):
        self.question_type = question_type
        self.question_full_score = question_full_score
        self.difficulty_of_question = difficulty_of_question
        self.question_score_state = question_score_state

