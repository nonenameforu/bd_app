from WorkTable import Table,allTables
from execute_in_bd import Execute
from abstactQuery import AbstractQuery
from finalquery import FinalQuery

class Select(AbstractQuery):

    def __init__(self) -> None:
        self.query ="Select"

    def newSelct(self,reqwest):
        self.ClearQuery()
        if isinstance(reqwest,Table) :
            fulpath = reqwest.GetAllFullPathSample()
            self.__GenerteSelect(fulpath)
            self.query = self.query[:-1] 

        elif (isinstance(reqwest,list)):
            for object in reqwest :
                if (isinstance(object,Table)): # TODO Добавить обработку позапросов
                    self.__GenerteSelect(object.GetAllFullPathSample())

                elif(isinstance(object,FinalQuery)):
                    self.__GenerteSelect(str(object))
            self.query = self.query[:-1]  

        elif (isinstance(reqwest,Select)):
            self.query +="("+str(reqwest)+")" 

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




