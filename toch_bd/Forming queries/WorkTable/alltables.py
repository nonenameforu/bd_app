from .table import Table

class allTables:
    def __init__(self) -> None:
        addresClient = {
            "Address":"addres"
            }
        addresFilial = {
            "Address":"addres"
            }
        agreement = {
            "Id":"id",
            "Amaunt":"amaunt",
            "Agreement":"agreement",
            "Filial":"filial",
            "Client":"client",
            "Employee":"emloeement",
            "InsuranceCompany":"insurancecompany",
            "DateOfConclusion":"dateofconclusion",
            "TypeOfInsurance":"typeofinsurance",
            "MainOffice":"mainoffice"
        }
        allCity = {
            "City":"city"
            }
        contractDate = {
            "DateContract":"datecontract"
            }
        filial = {
            "City":"idcity",
            "Name":"name",
            "Address":"addres",
            "Telephone":"telephone",
            "Year":"year",
            "NumOfEmployeer":"numofemploeers",
            "Id":"id"
        }
        insuranceCompany = {
            "Id":"id",
            "Name":"name",
            "TypeProperty":"typeproperty"
        }
        license = {
            "Id":"id",
            "Photo":"photo",
            "EndDateLicense":"endlicense",
            "Number":"number"
        }
        mainOffice = {
            "City":"city",
            "Telephone":"phonecharacter",
            "Addres":"addres",
            "YearStart":"yearstart",
            "License":"license",
            "Id":"id"
        }
        numClient = {
            "Id":"id",
            "City":"idcity",
            "Address":"idaddres",
            "FIO":"fio",
            "Telephone":"telephone",
            "SocialStatus":"socialstatus"
        }
        numEmploee = {
            "Id":"id",
            "FIO":"fio"
        }
        self.__titeleTeble = {
            "addresclient":addresClient ,
            "addresfilial":addresFilial ,
            "agreement":agreement ,
            "allcity":allCity ,
            "contractdate":contractDate ,
            "filial":filial ,
            "insurancecompany":insuranceCompany ,
            "license":license ,
            "mainoffice":mainOffice ,
            "numclient":numClient ,
            "numemployee":numEmploee
        }

    def __ToTable(self,Title:str):
        return Table(Title,self.__titeleTeble[Title])

    def __getitem__ (self,Title:int) :
        i = 0
        for key in self.__titeleTeble.keys():
            if i == Title:
                return self.__ToTable(key)
            i = i+1
        raise IndexError("Не верное значение индекса "+str(Title))
    
    def GetItem(self,item:str):
        return self.__ToTable(item)
            

if __name__ == "__main__":
    table = allTables()
    print (table[0].GetAllFullPathSample())
