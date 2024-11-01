from abstactQuery import AbstractQuery
class FinalQuery(AbstractQuery): 
    def __init__(self) -> None:
        self.query = ""

    def __query(self,action:str,Title:str,column:str):
        self.query = f"{action} {column} as {Title}"
    
    def SUM(self,Title:str,column:str):
        self.__query("SUM",Title,column)
    
    def COUNT(self,Title:str,column:str):
        self.__query("COUNT",Title,column)
    
    def AVG(self,Title:str,column:str):
        self.__query("AVG",Title,column)

    def MAX(self,Title:str,column:str):
        self.__query("MAX",Title,column)
    
    def MIN(self,Title:str,column:str):
        self.__query("MIN",Title,column)

    def __str__(self) -> str:
        return self.query