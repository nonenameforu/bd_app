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

    def __join (self,join:str,firstOperand:str,signin:str,secondOperand:str):

        firstOperand = self.LeftTab.GetFullPathSample([firstOperand])[firstOperand]
        secondOperand = self.LeftTab.GetFullPathSample([secondOperand])[secondOperand]


        sign = {
            "more":">",
            "equal":"=",
            "less":"<"
        }
        self.query = f"""{join} JOIN {self.LeftTab.GetTitel()} ON {firstOperand} {sign[signin]} {secondOperand};"""
        print (self.query)

    def Inner(self,firstOperand:str,signin:str,secondOperand:str):
        self.__join("INNER",firstOperand,signin,secondOperand)

    def Left(self,firstOperand:int,signin:str,secondOperand:str):
        self.__join("LEFT",firstOperand,signin,secondOperand)

    def Right(self,firstOperand:int,signin:str,secondOperand:str):
        self.__join("RIGHT",firstOperand,signin,secondOperand)

    def __str__(self) -> str:
        return self.query

    def __add__(self,other):
        if isinstance(other, AbstractQuery):
            if self.query != "":
                return (self.query+"\n" + str(other))
            else:
                raise ValueError("Невозможно сложить с пустым с пустым запросом")
        raise TypeError("Невозможно сложить с объектом другого типа")
    


if __name__ == "__main__":
    q = Select()
    tab = allTables()
    filal = tab.GetItem("filial")
    filal.SetTable(filal.GetTitel(),filal.GetSample(["City"]))
    numclient = tab.GetItem("numclient")
    numclient.SetTable(numclient.GetTitel(),numclient.GetSample(["FIO","SocialStatus"]))
    q.From([filal,numclient])
    b = Join((tab.GetItem("numclient")),(tab.GetItem("filial")))
    b.Inner("City","equal","City")
    print (q+b)
    bd = Execute()
    print(bd.execIO(q+b))
