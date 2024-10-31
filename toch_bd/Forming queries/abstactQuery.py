from abc import ABC ,abstractclassmethod
class AbstractQuery(ABC):
    def __init__(self) -> None:
        self.query =""