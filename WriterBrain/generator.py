from abstractexpert import AbstractExpert
import random

class ContentGenerator(AbstractExpert):
    @property
    def is_eager_to_contribute(self) -> bool:
        return True

    def contribute(self) -> None:
        self.blackboard.common_state["problems"] += random.randint(1, 10)
        self.blackboard.common_state["suggestions"] += random.randint(1, 10)
        self.blackboard.common_state["contributions"] += [self.__class__.__name__]
        self.blackboard.common_state["progress"] += random.randint(1, 2)

