from WorkTable import Table,allTables
from execute_in_bd import Execute
from abstactQuery import AbstractQuery

class Select(AbstractQuery):

    def __init__(self) -> None:
        self.query ="Select"

    def newSelct(self,tab):
        self.ClearQuery()
        if isinstance(tab,Table) :
            fulpath = tab.GetAllFullPathSample()
            self.__GenerteSelect(fulpath)
            self.query = self.query[:-1] 

        elif (isinstance(tab,list) and isinstance(tab[0],Table)):
            for table in tab :
                self.__GenerteSelect(table.GetAllFullPathSample())
            self.query = self.query[:-1]  

        elif (isinstance(tab,Select)):
            self.query +="("+str(tab)+")" 

    def From(self,tab):
        self.query = self.query + "\nFrom "+tab.GetTitel() 
        

    def Where(self,tab):
        self.query += "\nWhere "+tab # TODO сделать нормальныйй where
                
         
    def __GenerteSelect(self,Allfulpath:dict):
        for path in Allfulpath :
            self.query +=" "+Allfulpath[path]+","

    def __str__(self) -> str:
        return self.query


    def __add__(self,other):
            if isinstance(other, AbstractQuery):
                if self.query != "Select":
                    return (self.query+"\n" + str(other))
                else:
                    raise ValueError("Невозможно сложить с пустым с пустым запросом")
            raise TypeError("Невозможно сложить с объектом другого типа")
    
    def ClearQuery(self):
        self.query = "Select"


if __name__ == "__main__":
    q = Select()
    tab = allTables()
    tabs = [tab[5],tab[6]]
    q.newSelct(tabs)
    q.From(tab[5])

    b = Select()
    b.newSelct(q)
    b.From(tab[6])

    print (b)




