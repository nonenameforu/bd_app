from .table import Table

class allTables:
    def __init__(self) -> None:
        addresClient = ["addres"]
        addresFilial = ["addres"]
        agreement = {
            "Id":"id",
            "Amaunt":"amaunt",
            "Agreement":"agreement",
            "Filial":"filial",
            "Client":"client",
            "Emploee":"emloeement",
            "insurancecompany",
            "dateofconclusion",
            "typeOfInsurance",
            "mainoffice"
        }
        allCity = ["city"]
        contractDate = ["datecontract"]
        filial = [
            "idcity",
            "name",
            "addres",
            "telephone",
            "year",
            "numofemploeers",
            "id"
        ]
        insuranceCompany = [
            "id",
            "name",
            "typeproperty"
        ]
        license = [
            "id",
            "photo",
            "endlicense",
            "number"
        ]
        mainOffice = [
            "city",
            "phonecharacter",
            "addres",
            "yearstart",
            "license",
            "id"
        ]
        numClient = [
            "id",
            ""
            "idaddres",
            "idclient",
            "idaddres",
            "fio",
            "telephone",
            "socialstatus"
        ]
        numEmploee = [
            "id",
            "fio"
        ]
        self.__titeleTeble = {
            "addresclient":addresClient ,
            "addresfilial":addresFilial ,
            "agreement":agreement ,
            "allcity":allCity ,
            "contractdate":contractDate ,
            "filial":filial ,
            "insrancecompany":insuranceCompany ,
            "license":license ,
            "mainoffice":mainOffice ,
            "numclient":numClient ,
            "numemployee":numEmploee
        }

    def __ToTable(self,Title:str):
        return Table(Title,self.__titeleTeble[Title])

    def __getitem__ (self,Title:int) :
        match (Title):
            case 0:
                return self.__ToTable("addresclient")
            case 1:
                return  self.__ToTable("addresfilial")
            case 2: 
                return  self.__ToTable("agreement")
            case 3:
                return  self.__ToTable("allcity")
            case 4:
                return  self.__ToTable("contractdate")
            case 5:
                return  self.__ToTable("filial")
            case 6:
                return  self.__ToTable("insrancecompany")
            case 7:
                return  self.__ToTable("license")
            case 8:
                return  self.__ToTable("mainoffice")
            case 9:
                return  self.__ToTable("numclient")
            case 10:
                return  self.__ToTable("numemployee")
    
    def GetItem(self,item:str):
        return self.__ToTable(item)
            

if __name__ == "__main__":
    table = allTables()
    print (table[0].GetAllFullPathSample())
