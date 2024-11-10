

class Table:
    def __init__(self, title: str, fields: dict) -> None:
        self.__title = title
        self.__fields = fields

    def GetSample(self, sample: list) -> dict:
        new_fields = {}
        for key in sample:
            if key in self.__fields:
                new_fields[key] = self.__fields[key]
        return new_fields
    
    def GetAllSample(self) -> dict:
        return self.__fields
    
    def GetFullPathSample(self, sample: list) -> dict:
        new_fields = {}
        for key in sample:
            if key in self.__fields:
                new_fields[key] = f"{self.__title}.{self.__fields[key]}"
        return new_fields
    
    def GetAllFullPathSample(self) -> dict:
        return {key: f"{self.__title}.{value}" for key, value in self.__fields.items()}
    
    def GetTitel(self) -> str:
        return self.__title

    def SetTable(self, title: str, fields: dict) -> None:
        self.__title = title
        self.__fields = fields

    def getfield(self):
        return self.__fields

    # def __getitem__(self):


