

class Table :
    def __init__(self, Title:str,Fields:map) -> None:
        self.__Title = Title
        self.__Fields = Fields

    def GetSample (self,sample:list) -> map:
        newFilds = {}
        for key in sample:
            newFilds[key] = self.__Fields[key]
        return newFilds
    
    def GetAllSample(self) -> map:
        return self.__Fields
    
    def GetFullPathSample(self,sample:list) -> map:
        newFilds = {}
        for key in sample:
            newFilds[key] = self.__Title+"."+self.__Fields[key]
        return newFilds
    
    def GetAllFullPathSample(self) -> map:
        return self.__Fields
    
    def GetTitel(self) -> str:
        return self.__Title

    def SetTable(self,Title:str,Fields:map) -> None:
        self.__Title = Title
        self.__Fields = Fields
    


