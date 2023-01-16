"""
https://en.wikipedia.org/wiki/Blackboard_system
"""
from __future__ import annotations
from abstractexpert import AbstractExpert

import random

COMMON_STATES = {
    'outline': list(),
    'sentiment':'', # Sentiment to be counted only after full article is created
    'fp_count':0, # First person counter
    'vocabulary_quality':0, # We would want to improve this score upwards 
    'add_observation':False, # Do not Add any observation until the whole content is generated
    'generate_content':True, # Initial state should be towards creating a content, turn to False only if full article is created
    'article_created': False # is the full article created?

}
class Blackboard:
    def __init__(self) -> None:
        self.experts = []
        self.common_state = {
            "problems": 0,
            "suggestions": 0,
            "contributions": [],
            "progress": 0,  # percentage, if 100 -> task is finished
        }

    def add_expert(self, expert: AbstractExpert) -> None:
        self.experts.append(expert)

def main():
    """
    >>> blackboard = Blackboard()
    >>> blackboard.add_expert(Student(blackboard))
    >>> blackboard.add_expert(Scientist(blackboard))
    >>> blackboard.add_expert(Professor(blackboard))
    >>> c = Controller(blackboard)
    >>> contributions = c.run_loop()
    >>> from pprint import pprint
    >>> pprint(contributions)
    ['Student',
     'Student',
     'Student',
     'Student',
     'Scientist',
     'Student',
     'Student',
     'Student',
     'Scientist',
     'Student',
     'Scientist',
     'Student',
     'Student',
     'Scientist',
     'Professor']
    """


if __name__ == "__main__":
    random.seed(1234)  # for deterministic doctest outputs
    import doctest

    doctest.testmod()