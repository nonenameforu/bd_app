
class Term:
    def __init__(self,First:str,Second:str,sign="") -> None:
        self.fistOperand = First
        self.secondOperand = Second
        self.sign = sign

    def SelectTerm(self,select:str):
        sign = {
            "more":">",
            "equal":"=",
            "less":"<"
        }
        return Term(self.fistOperand,self.secondOperand,sign[select])
        