class ModelError(Exception):
    """LLM model not supported"""


class AnswerFormattingError(Exception):
    """LLM answer is not formatted as wonted"""
