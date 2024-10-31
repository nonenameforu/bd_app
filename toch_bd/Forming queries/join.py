from TermOperand import Term
from abstactQuery import AbstractQuery
from WorkTable import Table,allTables
from selectsql import Select
from execute_in_bd import Execute


class Join(AbstractQuery):
    def __init__(self,LeftTab:Table,RightTab:Table):
        self.query = ""
        self.LeftTab = LeftTab
        self.RightTab = RightTab

    def __join (self,join:str,firstOperand:int,signin:str,secondOperand:str):
        firstOperand = [firstOperand]
        secondOperand = [secondOperand]
        sign = {
            "more":">",
            "equal":"=",
            "less":"<"
        }
        self.query = f"""{join} JOIN {self.LeftTab.GetTitel()} ON {self.LeftTab.GetFullPathSample(firstOperand)[0]} {sign[signin]} {self.RightTab.GetFullPathSample(secondOperand)[0]};"""

    def Inner(self,firstOperand:int,signin:str,secondOperand:int):
        self.__join("INNER",firstOperand,signin,secondOperand)

    def Left(self,firstOperand:int,signin:str,secondOperand:str):
        self.__join("LEFT",firstOperand,signin,secondOperand)

    def Right(self,firstOperand:int,signin:str,secondOperand:str):
        self.__join("RIGHT",firstOperand,signin,secondOperand)

    def __add__(self,other):
        if isinstance(other, AbstractQuery):
            if self.query != "":
                return (self.query+"\n" + other.query)
            else:
                raise ValueError("Невозможно сложить с пустым с пустым запросом")
        raise TypeError("Невозможно сложить с объектом другого типа")
    


if __name__ == "__main__":
    q = Select()
    tab = allTables()
    filal = tab[5]
    filal.SetTable(filal.GetTitel(),filal.GetSample([0]))
    numclient = tab.GetItem("numclient")
    numclient.SetTable(numclient.GetTitel(),numclient.GetSample([3,5]))
    q.From([filal,numclient])
    b = Join((tab.GetItem("numclient")),(tab.GetItem("filial")))
    b.Inner(0,"equal",1)
    print (q+b)
    bd = Execute()
    bd.execIO(q+b)
