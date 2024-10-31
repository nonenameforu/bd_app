from WorkTable import Table,allTables
from execute_in_bd import Execute
from abstactQuery import AbstractQuery

class Select(AbstractQuery):

    def __init__(self) -> None:
        self.query ="Select"

    def From(self,tab):
        if isinstance(tab,Table) :
            fulpath = tab.GetAllFullPathSample()
            self.__GenerteSelect(fulpath)
            self.query = self.query[:-1] + "\nFrom "+tab.GetTitel() 
        elif (isinstance(tab,list) and isinstance(tab[0],Table)):
            for table in tab :
                self.__GenerteSelect(table.GetAllFullPathSample())
            self.query = self.query[:-1] + "\nFrom "+tab[0].GetTitel() 
                
         
    def __GenerteSelect(self,Allfulpath:list):
        for path in Allfulpath :
            self.query +=" "+path+","


    def __add__(self,other):
            if isinstance(other, AbstractQuery):
                if self.query != "Select":
                    return (self.query+"\n" + other.query)
                else:
                    raise ValueError("Невозможно сложить с пустым с пустым запросом")
            raise TypeError("Невозможно сложить с объектом другого типа")
    
    def ClearQuery(self):
        self.query = "Select"


if __name__ == "__main__":
    q = Select()
    tab = allTables()
    tabs = [tab[5],tab[6]]
    q.From(tabs)
    b = Select()
    b.From(tab[6])
    print (q+b)




