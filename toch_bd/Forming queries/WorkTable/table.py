

class Table :
    def __init__(self, Title:str,Fields:list) -> None:
        self.__Title = Title
        self.__Fields = Fields

    def GetSample (self,sample:list) ->list:
        newFilds = []
        for i in range (len(sample)):
            newFilds.append(self.__Fields[sample[i]])
        return newFilds
    
    def GetAllSample(self) -> list:
        return self.__Fields
    
    def GetFullPathSample(self,sample:list) -> list:
        newFilds = []
        for i in range (len(sample)):
            newFilds.append(self.__Title+"."+self.__Fields[sample[i]])
        return newFilds
    
    def GetAllFullPathSample(self) -> list:
        newFilds = []
        for i in range (len(self.__Fields)):
            newFilds.append(self.__Title+"."+self.__Fields[i])
        return newFilds
    
    def GetTitel(self)->str:
        return self.__Title

    def SetTable(self,Title:str,Fields:list):
        self.__Title = Title
        self.__Fields = Fields
    


