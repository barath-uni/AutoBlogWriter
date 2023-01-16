
from brain import Blackboard

class Controller:
    def __init__(self, blackboard: Blackboard) -> None:
        self.blackboard = blackboard

    def run_loop(self):
        """
        This function is a loop that runs until the progress reaches 100.
        It checks if an expert is eager to contribute and then calls its contribute method.
        """
        while self.blackboard.common_state["progress"] < 100:
            for expert in self.blackboard.experts:
                if expert.is_eager_to_contribute:
                    expert.contribute()
        return self.blackboard.common_state["contributions"]
