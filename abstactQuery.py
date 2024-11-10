from abc import ABC 
class AbstractQuery(ABC):
    def __init__(self) -> None:
        self.query =""