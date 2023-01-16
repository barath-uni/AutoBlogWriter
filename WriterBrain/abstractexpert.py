import abc

class AbstractExpert(metaclass=abc.ABCMeta):
    def __init__(self, blackboard: Blackboard) -> None:
        self.blackboard = blackboard

    @property
    @abc.abstractmethod
    def is_eager_to_contribute(self):
        raise NotImplementedError("Must provide implementation in subclass.")

    @abc.abstractmethod
    def contribute(self):
        raise NotImplementedError("Must provide implementation in subclass.")
