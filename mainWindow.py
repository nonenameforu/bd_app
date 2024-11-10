import tkinter as tk
from tkinter import ttk
from table import Table
from tkinter import messagebox
from tkinter import filedialog
from uiTable import uiTable
from Tables import allTables
from execute_in_bd import Execute
from selectsql import Select
from datetime import date
from datetime import datetime
from tkcalendar import DateEntry
from fileChoserTk import FileChooserButton
from PIL import Image
from PIL import ImageTk
import io
from io import BytesIO
import base64
import pandas as pd


class mainWindow:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Приложение с вкладками и таблицами")
        self.root.geometry("600x400")
        self.root.minsize(1000, 600)
        self.MyTables = {}
        self.connect = Execute()

    def exec(self):
        self.createTabs()
        self.bottom_frame = self.creteBottomFrame()
        self.createButtons()

    def Start(self):
        self.root.mainloop()

    def creteBottomFrame(self):
        # Создаем фрейм внизу окна
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        return bottom_frame

    def createTabs(self):
        # Создаем виджет для вкладок
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")
        tables = allTables()

        i = 0
        for tabs in tables:
            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab,text=tabs.GetTitel())
            titles = tabs.getfield()
            titles = titles.keys()
            title = []
            for collumn in titles:
                title.append (collumn)
            tree = ttk.Treeview(tab,columns = title,show="headings")
            if tabs.GetTitel() == "license":
                tree.bind("<Double-ButtonPress-1>", self.double_click)
            tabs = uiTable(tabs,tree,tab)
            self.MyTables[i] = tabs
            for collumn in title:
                self.MyTables[i].tree.heading(collumn, text=collumn)
            self.MyTables[i].tree.pack(expand = True, fill = "both")
            self.filingTables(tabs.baseTable.GetTitel(),i)
            i +=1

    def createButtons(self):
        # Добавляем кнопки
        addButton = ttk.Button(self.bottom_frame, text="add",command=self.addButton)
        addButton.pack(side="left", padx=(0, 10))

        deleteButton = ttk.Button(self.bottom_frame, text="delete",command=self.deleteButton)
        deleteButton.pack(side="left")

        redactButton = ttk.Button(self.bottom_frame, text="redact",command=self.redactButton)
        redactButton.pack(side="left")

        refreshButton = ttk.Button(self.bottom_frame, text="refresh",command=self.refreshButton)
        refreshButton.pack(side="left")

        statesticButton = ttk.Button(self.bottom_frame, text="statistic",command=self.statisticButton)
        statesticButton.pack(side="left")

        self.serchEntry = ttk.Entry(self.bottom_frame)
        self.serchEntry.pack(side="left",padx="45",fill="x")
        
        searchButton = ttk.Button(self.bottom_frame,text="search",command=self.serch)
        searchButton.pack(side="left")

        ressetButton = ttk.Button(self.bottom_frame,text="resset search",command=self.ressetSearch)
        ressetButton.pack(side="left")

        geneareteTable = ttk.Button(self.bottom_frame,text="generate Exel",command=self.GenerateExelFilie)
        geneareteTable.pack(side="left")


    def filingTables(self,name:str,num:int):
        query = Select()
        tables = allTables()
        tables = tables.GetItem(name)
        query.newSelct(tables)
        query.From(tables)
        self.connect.reconect()
        result = self.connect.execIO(str(query))
        for row in result:
            self.MyTables[num].tree.insert("", "end",values=row)

    def addButton(self):
        note = ".!notebook.!frame"
        match (self.notebook.select()):
            case ".!notebook.!frame":
                self.addAddresclient()
            case ".!notebook.!frame2":
                self.addAgreement()
            case ".!notebook.!frame3":
                self.addCity()
            case ".!notebook.!frame4":
                self.addContractDate()
            case ".!notebook.!frame5":
                self.addFilial()
            case ".!notebook.!frame6":
                self.addInsuranceCompany()
            case ".!notebook.!frame7":
                self.addLicense()
            case ".!notebook.!frame8":
                self.addMainOffice()
            case ".!notebook.!frame9":
                self.addNumClient()
            case ".!notebook.!frame10":
                self.addNumEmployeer()

    def addAddresclient(self): 
        def addButton():
                self.connect.reconect()
                try:
                    self.connect.exec(f"""Insert Into addresclient Values ({address.get()})""")
                    new_window.destroy()
                except:
                    messagebox.showwarning("Error","Ваш запрос не был отпавлен")
        new_window = self.newWindow("add Address","250x200")
        address = self.newEntry(new_window,"addres")
        Button = self.newButton(new_window,"add",addButton)
        
    def newWindow(self,name:str,size:str):
        new_window = tk.Toplevel(self.root)
        new_window.title(name)
        new_window.geometry(size)
        new_window.attributes("-topmost", True)
        return new_window

    def addAgreement(self): # TODO добавить проверку на пустоту
        def addButton():
            self.connect.reconect()
            id = self.connect.execIO("Select Max(agreement.id) From agreement")
            
            try:
                if int(amaunt.get()) >= 15_000:
                    numAmaunt = int(amaunt.get())
                else:
                    messagebox.showwarning("Error","Слишком маленькая цена за договор")
            except:
                messagebox.showwarning("Error","Введена не цифра")

            filialId = self.GetAttribute("Select id From filial where name =",filial)
            clientId = self.GetAttribute("Select id From numclient where fio = ",client)
            employeeId = self.GetAttribute("Select id From numemployee where fio = ",employee)
            
            self.connect.reconect()
            insuranceName = self.connect.execIO(f"Select id From insurancecompany where name = '{insurance.get()}'")
            insuranceName = insuranceName[0][0]

            self.connect.reconect()
            date = self.connect.execIO(f"Select datecontract From contractdate where datecontract = '{dateofcoclusion.get_date()}'")
            if len(date) == 0:
                self.connect.reconect()
                self.connect.exec(f"Insert Into contractdate Values('{dateofcoclusion.get_date()}')")


            query = f"""
        INSERT INTO agreement VALUES (
            {id[0][0]+1}, {numAmaunt}, '{agreement.get("1.0", "2.0")}',
            (SELECT id FROM filial WHERE id = {filialId}),
            (SELECT id FROM numclient WHERE id = {clientId}),
            (SELECT id FROM numemployee WHERE id = {employeeId}),
            (SELECT id FROM insurancecompany WHERE id = {insuranceName}),
            (SELECT datecontract FROM contractdate WHERE datecontract = '{dateofcoclusion.get_date()}'),
            '{TyepOfInsurance.get()}',
            (SELECT id FROM mainoffice WHERE id = 0)
        );
    """
            self.connect.reconect()
            self.connect.exec(query)
            new_window.destroy()
        
        new_window = self.newWindow("add agreement", "550x750")
        amaunt = self.newEntry(new_window,"amaunt")
        agreement = self.newTextBox(new_window,"agreement")
        filial = self.newCombobox(new_window,"filial","Select filial.name From filial")
        client = self.newCombobox(new_window,"client","Select numclient.fio From numclient")
        employee = self.newCombobox(new_window,"employee","Select numemployee.fio From numemployee")
        insurance = self.newCombobox(new_window,"InsuranceCompany","Select insurancecompany.name from insurancecompany")
        dateofcoclusion = self.newDate(new_window,"Date Of Conclusion")
        TyepOfInsurance = ["Медицинское страхование","Автомобильное страхование",
        "Страхование жизни","Имущественное страхование",
        "Страхование от несчастных случаев","Пенсионное страхование","Страхование путешествий",
        "Страхование бизнеса","Страхование ответственности","Страхование на случай потери работы",
        "Ипотечное страхование","Страхование домашних животных","Страхование от стихийных бедствий"]
        TyepOfInsurance = self.newCombobox(new_window,"Type Of Insurance",TyepOfInsurance)

        Button = self.newButton(new_window,"add",addButton)




    def newEntry(self,window,text):
        Lable = tk.Label(window,text=text)
        Lable.pack(fill="both")
        Entry = tk.Entry(window)
        Entry.pack(fill="both")
        return Entry
    
    def newTextBox(self,window,text):
        Lable = tk.Label(window,text=text)
        Lable.pack()
        Text = tk.Text(window)
        Text.pack()
        return Text

    def newCombobox(self,window,text,query)->ttk.Combobox:
        if isinstance(query,str):
            Lable = tk.Label(window,text=text)
            Lable.pack(fill="both")
            allFilial = self.fillingCombobox(query)
            ComboBox =ttk.Combobox(window,values=allFilial ,state="readonly")
            ComboBox.pack(fill="both")
            return ComboBox
        elif isinstance(query,list):
            Lable = tk.Label(window,text=text)
            Lable.pack(fill="both")
            ComboBox =ttk.Combobox(window,values=query,state="readonly")
            ComboBox.pack(fill="both")
            return ComboBox

    def fillingCombobox(self,query):
        allItem = []
        self.connect.reconect()
        result = self.connect.execIO(query)
        for item in result:
            allItem.append(item[0])
        return allItem
    
    def newButton(self,window,text,func):
        Button = tk.Button(window,text=text,command=func)
        Button.pack()
        return Button

    def newDate(self,window,text):
        Lable = tk.Label(window,text=text)
        Lable.pack()
        Date = DateEntry(window)
        Date.pack()
        return Date

    def GetAttribute(self,query,obj):
        self.connect.reconect()
        result = self.connect.execIO(query+"'"+obj.get()+"'")
        result = int(result[0][0])
        return result
    
    def addCity(self): 
        def addButton():
            self.connect.reconect()
            result = self.connect.execIO(f"Select city From allcity where city = '{city.get()}'")
            if len(result) == 0 :
                if len(city.get())<30:
                    self.connect.reconect()
                    self.connect.exec(f"Insert Into allcity Values('{city.get()}')")
                else:
                    messagebox.showwarning("Error","Сликом длинное назваение города")
            else:
                 messagebox.showinfo("Info","Такой город уже есть")
                 return 0
            
            new_window.destroy()
        new_window = self.newWindow("Add City","300x250")
        city = self.newEntry(new_window,"City")
        Button = self.newButton(new_window,"add",addButton)

    def addContractDate(self): 
        def addButton():
            self.connect.reconect()
            result = self.connect.execIO(f"Select datecontract From contractdate where datecontract = '{Date.get_date()}'")
            if len(result) == 0 :
                self.connect.reconect()
                self.connect.exec(f"Insert Into contractdate Values('{Date.get_date()}')")
            else:
                 messagebox.showinfo("Info","Такая дата уже есть")
                 return 0
            new_window.destroy()
        new_window = self.newWindow("add Contract Date","300x250")
        Date = self.newDate(new_window,"Contract date")
        Button = self.newButton(new_window,"add",addButton)

    def addFilial(self): # TODO добавить проверку на пустоту
        def addButton():
            Year = datetime.now().year
            id = self.connect.execIO("Select Max(filial.id) From filial")
            id = id[0][0]+1
            try:
                if len(Telephone.get())== 11:
                    tel = int(Telephone.get())
                else:
                    messagebox.showwarning("Error","Слишком много цифр")
                    return 0
            except:
                messagebox.showwarning("Error","Вы ввели не номер")

            self.connect.reconect()
            result = self.connect.execIO(f"Select telephone From filial Where telephone = '{tel}'")
            if len(result) != 0:
                messagebox.showwarning("Error","Такой номер уже есть")
                return 0
            
            if len(Name.get()) < 30 :
                self.connect.reconect()
                result = self.connect.execIO(f"Select name From filial Where name = '{Name.get()}' ")
            else :
                messagebox.showwarning("Error","Слишком длинное название филиала")
                return 0

            if len(Addres.get()) >50:
                messagebox.showwarning("Error","Слишком длинное название улицы")

            employeeId = self.GetAttribute("Select id From numemployee where fio = ",Employee)
            query = f"""
            INSERT INTO filial VALUES(
            (SELECT city FROM allcity WHERE city = '{City.get()}'),
            '{Name.get()}','{Addres.get()}','{tel}',{Year},
            (Select id From numemployee where id = {employeeId}),
            {id})
            """
            self.connect.reconect()
            self.connect.exec(query)
            new_window.destroy()

        new_window = self.newWindow("add Filial","300x350")
        City = self.newCombobox(new_window,"City","Select allcity.city From allcity")
        Name = self.newEntry(new_window,"Name")
        Addres = self.newEntry(new_window,"Addres")
        Telephone = self.newEntry(new_window,"Telephone")
        Employee = self.newCombobox(new_window,"Employee","Select numemployee.fio From numemployee")
        Button = self.newButton(new_window,"add",addButton)

    def addInsuranceCompany(self): # TODO добавить проверку на пустоту
        def addButton():
            self.connect.reconect()
            id = self.connect.execIO("Select max(id) From insurancecompany")
            id = id[0][0] + 1
            if len(Name.get())>50:
                messagebox.showerror("Error","Слишком длинное имя")
                return 0 
            self.connect.reconect()
            result = self.connect.execIO(f"Select name From insurancecompany Where name = '{Name.get()}'")
            if len(result) > 0 :
                messagebox.showwarning("Error","Такое имя уже есть")
                return 0
            query = f"""
                INSERT INTO insurancecompany VALUES (
                {id},
                '{Name.get()}',
                '{TypeProperty.get()}')
             """
            self.connect.reconect()
            self.connect.exec(query)
            new_window.destroy()
        new_window = self.newWindow("add Insurance Company","300x250")
        Name = self.newEntry(new_window,"Name")
        Property = ["Частная собственность",
        "Государственная собственность",
        "Смешанная собственность",
        "Иностранная собственность"]
        TypeProperty = self.newCombobox(new_window,"Type Property",Property)
        Button = self.newButton(new_window,"add",addButton)

    def addLicense(self):
        def addButton():
            self.connect.reconect()
            id = self.connect.execIO("Select max(id) From license")
            id = id[0][0] + 1
            path = ButtonImage.get()
            date = EndDate.get_date()
            num = Number.get()
            self.connect.reconect()
            res = self.connect.execIO("Select max(endlicese) From license")
            res = res[0][0]
            today = date.today()
            if date < res and today > date:
                messagebox.showwarning("Error","Не верная дата новой лицензии")
            try:
                int(num)
                print(path)
                print(len(path))
                if len(path) != 0 and len(num) != 0:
                    image_bytes = ""
                    with Image.open(path) as image:
                        # Создаем буфер для хранения битового представления
                        byte_stream = io.BytesIO()
                        # Сохраняем изображение в буфер в формате PNG
                        image.save(byte_stream, format="PNG")
                        # Получаем байтовое представление
                        image_bytes = byte_stream.getvalue()
                    query = "INSERT INTO license VALUES (%s, %s, %s, %s)"
                    values = (id,image_bytes,date,num)
                    self.connect.reconect()
                    self.connect.execTwoArguments(query,values)
                    new_window.destroy()
                else:
                    messagebox.showinfo("Info","Заполните поля")
            except:
                messagebox.showwarning("Error","Вы ввели не число в number")
            
        new_window = self.newWindow("add License","300x250")
        ButtonImage = FileChooserButton(new_window)
        ButtonImage.pack()
        EndDate = self.newDate(new_window, "End Date")
        Number = self.newEntry(new_window, "Number")
        Button = self.newButton(new_window,"add",addButton)

    def addMainOffice(self):
        def addButton():
            self.connect.reconect()
            id = self.connect.execIO("Select max(id) From mainoffice")
            id = id[0][0] + 1
            self.connect.reconect()
            licenseId = self.connect.execIO("Select id From license Where endlicese = (Select max(endlicese) From license)")
            licenseId = licenseId[0][0] + 1
            try:
                tel = Telephone.get() 
                adress = Addres.get()
                year = YearStart.get()
                int(tel)
                if len(tel) <= 11 and len(adress) <= 30 and int(year)< 2024:
                    query = f"""
                    Insert Into mainoffice Values('{City.get()}','{tel}','{adress}',{year},{licenseId},{id}
                    )
                    """
                    self.connect.reconect()
                    self.connect.exec(query)
                    new_window.destroy()
                else:
                    messagebox.showwarning("Error","введите информацию верно")
            except:
                messagebox.showwarning("Error","Вы ввели не число в Telephone или Year Start")
        new_window = self.newWindow("Add Main Office","300x500")
        City = self.newCombobox(new_window,"City","Select city From allcity ")
        Telephone  = self.newEntry(new_window,"Telephone")
        Addres = self.newEntry(new_window,"Addres")
        YearStart = self.newEntry(new_window,"Year Start")
        Button = self.newButton(new_window,"add",addButton)

    def addNumClient(self):
        def addButton():
            self.connect.reconect()
            id = self.connect.execIO("Select max(id) From numclient")
            id = id[0][0] + 1
            fio = Fio.get()
            socstatus = SocialStatus.get()
            city = City.get()
            try:
                tel = Telephone.get() 
                adress = Addres.get()
                int(tel)
                socstatus = int(socstatus)
                if len(tel) <= 11 and len(fio)<50 and socstatus>0 and socstatus<=1000:
                    query  =f"""
                    Insert Into numclient Values({id},'{city}','{adress}','{fio}','{tel}',{socstatus}
                    )
                    """
                    self.connect.reconect()
                    self.connect.exec(query)
                    new_window.destroy()
            except:
                messagebox.showwarning("Error","Вы ввели не число в Telephone")
        new_window = self.newWindow("Add Num Client","300x500")
        City = self.newCombobox(new_window,"City","Select city From allcity ")
        Addres = self.newCombobox(new_window,"Address","Select addres From addresclient")
        Fio = self.newEntry(new_window,"FIO")
        Telephone  = self.newEntry(new_window,"Telephone")
        SocialStatus = self.newEntry(new_window,"Social status")
        Button = self.newButton(new_window,"add",addButton)
        
    def addNumEmployeer(self):
        def addButton():
            self.connect.reconect()
            id = self.connect.execIO("Select max(id) From numemployee")
            id = id[0][0] + 1
            fio = FIO.get()
            if len(fio)<60:
                query = f"Insert Into numemployee Values( {id} ,'{fio}' )"
                self.connect.reconect()
                self.connect.exec(query)
                new_window.destroy()
        new_window = self.newWindow("Add Num Client", "300x200")
        FIO = self.newEntry(new_window,"FIO")
        Button = self.newButton(new_window,"add",addButton)



    def deleteButton(self): 
        note = ".!notebook.!frame"
        try:
            match (self.notebook.select()):
                case ".!notebook.!frame":
                    sel = self.MyTables[0].tree.selection()
                    sel = self.MyTables[0].tree.item(sel)['values']
                    query = f"DELETE FROM addresclient WHERE addres = '{sel[0]}'"
                case ".!notebook.!frame2":
                    sel = self.MyTables[1].tree.selection()
                    sel = self.MyTables[1].tree.item(sel)['values']
                    query = f"DELETE FROM agreement WHERE id = {sel[0]}"
                case ".!notebook.!frame3":
                    sel = self.MyTables[2].tree.selection()
                    sel = self.MyTables[2].tree.item(sel)['values']
                    query = f"DELETE FROM allcity WHERE city = '{sel[0]}'"
                case ".!notebook.!frame4":
                    sel = self.MyTables[3].tree.selection()
                    sel = self.MyTables[3].tree.item(sel)['values']
                    query = f"DELETE FROM contractdate WHERE datecontract = '{sel[0]}'"
                case ".!notebook.!frame5":
                    sel = self.MyTables[4].tree.selection()
                    sel = self.MyTables[4].tree.item(sel)['values']
                    query = f"DELETE FROM filial WHERE id = {sel[6]}"
                case ".!notebook.!frame6":
                    sel = self.MyTables[5].tree.selection()
                    sel = self.MyTables[5].tree.item(sel)['values']
                    query = f"DELETE FROM insurancecompany WHERE id = {sel[0]}"
                case ".!notebook.!frame7":
                    sel = self.MyTables[6].tree.selection()
                    sel = self.MyTables[6].tree.item(sel)['values']
                    query = f"DELETE FROM license WHERE id = {sel[0]}"
                case ".!notebook.!frame8":
                    sel = self.MyTables[7].tree.selection()
                    sel = self.MyTables[7].tree.item(sel)['values']
                    query = f"DELETE FROM mainoffice WHERE id = {sel[5]}"
                case ".!notebook.!frame9":
                    sel = self.MyTables[8].tree.selection()
                    sel = self.MyTables[8].tree.item(sel)['values']
                    query = f"DELETE FROM numclient WHERE id = {sel[0]}"
                case ".!notebook.!frame10":
                    sel = self.MyTables[9].tree.selection()
                    sel = self.MyTables[9].tree.item(sel)['values']
                    query = f"DELETE FROM numemployee WHERE id = {sel[0]}"
        except:
            pass   
        try:
            self.connect.reconect()
            self.connect.exec(query)    
        except:
            messagebox.showwarning("Error","Эту запись нельзя удалить")


    def refreshButton(self):
        tables = allTables()
        noteSelect = self.notebook.select()
        if ".!notebook.!frame" == noteSelect:
            tab = 0
        else :
            tab = int(noteSelect[-1]) - 1
            if tab == -1:
                tab = 9
        for item in self.MyTables[tab].tree.get_children():
            self.MyTables[tab].tree.delete(item)
        self.filingTables(tables[tab].GetTitel(),tab)


    def redactButton(self):
        def ForRedact(item,func):
            try:
                sel = self.MyTables[item].tree.selection()
                sel = self.MyTables[item].tree.item(sel)['values']
                sel[0]
                func(sel)
            except:
                pass
        note = ".!notebook.!frame"
        match (self.notebook.select()):
            case ".!notebook.!frame":
                ForRedact(0,self.redactAddresclient)
            case ".!notebook.!frame2":
                ForRedact(1,self.redactAgreement)
            case ".!notebook.!frame3":
                ForRedact(2,self.redactCity)
            case ".!notebook.!frame4":
                 ForRedact(3,self.redactCity)
            case ".!notebook.!frame5":
                ForRedact(4,self.redactFilial)
            case ".!notebook.!frame6":
                ForRedact(5,self.redactInsuranceCompany)
            case ".!notebook.!frame7":
                ForRedact(6,self.redactLicense)
            case ".!notebook.!frame8":
                ForRedact(7,self.redactMainOffice)
            case ".!notebook.!frame9":
                ForRedact(8,self.redactNumClient)
            case ".!notebook.!frame10":
                ForRedact(9,self.redactNumEmployeer)

    def redactAddresclient(self,dataSet): 
        def addButton():
                self.connect.reconect()
                try:
                    self.connect.exec(f"Update addresclient Set addres='{address.get()}' Where addres = '{address.get()}'")
                    new_window.destroy()
                except:
                    messagebox.showwarning("Error","Ваш запрос не был отпавлен")
        new_window = self.newWindow("redact Address","250x200")
        address = self.newEntry(new_window,"addres")
        address.insert(0,dataSet[0])
        Button = self.newButton(new_window,"redact",addButton)

    def redactAgreement(self,dataSet): 
        def addButton():
            id = dataSet[0]
            
            try:
                if int(amaunt.get()) >= 15_000:
                    numAmaunt = int(amaunt.get())
                else:
                    messagebox.showwarning("Error","Слишком маленькая цена за договор")
            except:
                messagebox.showwarning("Error","Введена не цифра")

            filialId = self.GetAttribute("Select id From filial where name =",filial)
            clientId = self.GetAttribute("Select id From numclient where fio = ",client)
            employeeId = self.GetAttribute("Select id From numemployee where fio = ",employee)
            
            self.connect.reconect()
            insuranceName = self.connect.execIO(f"Select id From insurancecompany where name = '{insurance.get()}'")
            insuranceName = insuranceName[0][0]

            self.connect.reconect()
            date = self.connect.execIO(f"Select datecontract From contractdate where datecontract = '{dateofcoclusion.get_date()}'")
            if len(date) == 0:
                self.connect.reconect()
                self.connect.exec(f"Insert Into contractdate Values('{dateofcoclusion.get_date()}')")


            query = f"""
            Update agreement Set amaunt = {numAmaunt},agreement = '{agreement.get("1.0", "2.0")}',
            filial = {filialId},
            client ={clientId},
            emploeement = {employeeId},
            insuancecompany = {insuranceName},
            dateofconclusion = '{dateofcoclusion.get_date()}',
            typeofinsuranse = '{TyepOfInsurance.get()}',
            mainoffice = 0 Where id = {id} 
    """
            self.connect.reconect()
            self.connect.exec(query)
            new_window.destroy()
        
        new_window = self.newWindow("add agreement", "550x750")
        amaunt = self.newEntry(new_window,"amaunt")
        amaunt.insert(0,str(dataSet[1]))
        agreement = self.newTextBox(new_window,"agreement")
        agreement.insert("2.0",dataSet[2])
        filial = self.newCombobox(new_window,"filial","Select filial.name From filial")
        self.connect.reconect()
        name = self.connect.execIO(f"select name from filial where id ={dataSet[3]}")
        name = name[0][0]
        filial.set(name)
        client = self.newCombobox(new_window,"client","Select numclient.fio From numclient")
        name = self.connect.execIO(f"select fio from numclient where id ={dataSet[4]}")
        name = name[0][0]
        client.set(name)
        employee = self.newCombobox(new_window,"employee","Select numemployee.fio From numemployee")
        name = self.connect.execIO(f"select fio from numemployee where id ={dataSet[5]}")
        name = name[0][0]
        employee.set(name)
        insurance = self.newCombobox(new_window,"InsuranceCompany","Select insurancecompany.name from insurancecompany")
        name = self.connect.execIO(f"select name from insurancecompany where id ={dataSet[6]}")
        name = name[0][0]
        insurance.set(name)
        dateofcoclusion = self.newDate(new_window,"Date Of Conclusion")
        TyepOfInsurance = ["Медицинское страхование","Автомобильное страхование",
        "Страхование жизни","Имущественное страхование",
        "Страхование от несчастных случаев","Пенсионное страхование","Страхование путешествий",
        "Страхование бизнеса","Страхование ответственности","Страхование на случай потери работы",
        "Ипотечное страхование","Страхование домашних животных","Страхование от стихийных бедствий"]
        TyepOfInsurance = self.newCombobox(new_window,"Type Of Insurance",TyepOfInsurance)
        TyepOfInsurance.set(dataSet[8])

        Button = self.newButton(new_window,"redact",addButton)

    def redactCity(self,dataSet): 
        def addButton():
            self.connect.reconect()
            result = self.connect.execIO(f"Select city From allcity where city = '{city.get()}'")
            if len(result) == 1 :
                if len(city.get())<30:
                    self.connect.reconect()
                    self.connect.exec(f"Update allcity Set city ='{city.get()}' where city = '{dataSet[0]}'")
                else:
                    messagebox.showwarning("Error","Сликом длинное назваение города")
            else:
                 messagebox.showinfo("Info","Такой город уже есть")
                 return 0
            
            new_window.destroy()
        new_window = self.newWindow("Add City","300x250")
        city = self.newEntry(new_window,"City")
        city.insert(0,dataSet[0])
        Button = self.newButton(new_window,"redact",addButton)

    def radactContractDate(self,dataSet):
        def addButton():
            self.connect.reconect()
            result = self.connect.execIO(f"Select datecontract From contractdate where datecontract = '{Date.get_date()}'")
            if len(result) == 1 :
                self.connect.reconect()
                self.connect.exec(f"Update contractdate Set contractdate ='{Date.get_date()}' where contractdate = '{dataSet[0]}'")
            else:
                 messagebox.showinfo("Info","Такая дата уже есть")
                 return 0
            new_window.destroy()
        new_window = self.newWindow("redact Contract Date","300x250")
        Date = self.newDate(new_window,"Contract date")
        Button = self.newButton(new_window,"redact",addButton)

    def redactFilial(self,dataSet):
        def addButton():
            Year = datetime.now().year
            id = self.connect.execIO("Select Max(filial.id) From filial")
            id = id[0][0]
            try:
                if len(Telephone.get())== 11:
                    tel = int(Telephone.get())
                else:
                    messagebox.showwarning("Error","Слишком много цифр")
                    return 0
            except:
                messagebox.showwarning("Error","Вы ввели не номер")
                
            self.connect.reconect()
            result = self.connect.execIO(f"Select telephone From filial Where telephone = '{tel}'")
            
            if len(Name.get()) < 30 :
                self.connect.reconect()
                result = self.connect.execIO(f"Select name From filial Where name = '{Name.get()}' ")
            else :
                messagebox.showwarning("Error","Слишком длинное название филиала")
                return 0

            if len(Addres.get()) >50:
                messagebox.showwarning("Error","Слишком длинное название улицы")

            employeeId = self.GetAttribute("Select id From numemployee where fio = ",Employee)
            query = f"""
            Update filial Set name = '{Name.get()}', addres = '{Addres.get()}',telephone = '{tel}',
            year = {Year},numofemploeers = {employeeId} where id = {dataSet[6]}
            """
            self.connect.reconect()
            self.connect.exec(query)
            new_window.destroy()

        new_window = self.newWindow("redact Filial","300x350")
        print (dataSet)
        City = self.newCombobox(new_window,"City","Select allcity.city From allcity")
        City.set(dataSet[0])
        Name = self.newEntry(new_window,"Name")
        Name.insert(0,dataSet[1])
        Addres = self.newEntry(new_window,"Addres")
        Addres.insert(0,dataSet[2])
        Telephone = self.newEntry(new_window,"Telephone")
        Telephone.insert(0,dataSet[3])
        Employee = self.newCombobox(new_window,"Employee","Select numemployee.fio From numemployee")
        self.connect.reconect()
        res = self.connect.execIO(f"Select fio From numemployee where id ={dataSet[5]}")
        res = res[0][0]
        Employee.set(res)
        Button = self.newButton(new_window,"redact",addButton)

    def redactInsuranceCompany(self, dataSet):
        def addButton():
            self.connect.reconect()
            id = self.connect.execIO("Select max(id) From insurancecompany")
            id = id[0][0] 
            if len(Name.get())>50:
                messagebox.showerror("Error","Слишком длинное имя")
                return 0 
            query = f"""
                Update insurancecompany Set name = '{Name.get()}',typeproperty = '{TypeProperty.get()}' Where id = {dataSet[0]} 
             """
            self.connect.reconect()
            self.connect.exec(query)
            new_window.destroy()
        print(dataSet)
        new_window = self.newWindow("add Insurance Company","300x250")
        Name = self.newEntry(new_window,"Name")
        Name.insert(0,dataSet[1])
        Property = ["Частная собственность",
        "Государственная собственность",
        "Смешанная собственность",
        "Иностранная собственность"]
        TypeProperty = self.newCombobox(new_window,"Type Property",Property)
        TypeProperty.set(dataSet[2])
        Button = self.newButton(new_window,"redact",addButton)

    def redactLicense(self,dataSet):
        def addButton():
            self.connect.reconect()
            id = self.connect.execIO("Select max(id) From license")
            id = id[0][0] + 1
            path = ButtonImage.get()
            date = EndDate.get_date()
            num = Number.get()
            self.connect.reconect()
            res = self.connect.execIO("Select max(endlicese) From license")
            res = res[0][0]
            today = date.today()
            if date < res and today > date:
                messagebox.showwarning("Error","Не верная дата новой лицензии")
            try:
                int(num)
                print(path)
                print(len(path))
                if len(path) != 0 and len(num) != 0:
                    image_bytes = ""
                    with Image.open(path) as image:
                        # Создаем буфер для хранения битового представления
                        byte_stream = io.BytesIO()
                        # Сохраняем изображение в буфер в формате PNG
                        image.save(byte_stream, format="PNG")
                        # Получаем байтовое представление
                        image_bytes = byte_stream.getvalue()
                    query = "Update license Set photo=%s ,endlicense=%s,numer=%s Where id = %s"
                    values = (image_bytes,date,num,dataSet[0])
                    self.connect.reconect()
                    self.connect.execTwoArguments(query,values)
                    new_window.destroy()
                else:
                    messagebox.showinfo("Info","Заполните поля")
            except:
                messagebox.showwarning("Error","Вы ввели не число в number")
            
        new_window = self.newWindow("redact License","300x250")
        ButtonImage = FileChooserButton(new_window)
        ButtonImage.pack()
        EndDate = self.newDate(new_window, "End Date")
        Number = self.newEntry(new_window, "Number")
        Number.insert(0,dataSet[3])
        Button = self.newButton(new_window,"redact",addButton)

    def redactMainOffice(self,dataSet):
        def addButton():
            self.connect.reconect()
            id = self.connect.execIO("Select max(id) From mainoffice")
            id = id[0][0]
            self.connect.reconect()
            licenseId = self.connect.execIO("Select id From license Where endlicese = (Select max(endlicese) From license)")
            licenseId = licenseId[0][0] 
            try:
                tel = Telephone.get() 
                adress = Addres.get()
                year = YearStart.get()
                int(tel)
                if len(tel) <= 11 and len(adress) <= 30 and int(year)< 2024:
                    query = f"""
                    Update mainoffice Set city='{City.get()}',phonecharacter='{tel}',addres ='{adress}',
                    yearstart = '{year}',license = {licenseId} where id = {id} 
                    """
                    self.connect.reconect()
                    self.connect.exec(query)
                    new_window.destroy()
                else:
                    messagebox.showwarning("Error","введите информацию верно")
            except:
                messagebox.showwarning("Error","Вы ввели не число в Telephone или Year Start")
        new_window = self.newWindow("Redact Main Office","300x500")
        City = self.newCombobox(new_window,"City","Select city From allcity ")
        City.set(dataSet[0])
        Telephone  = self.newEntry(new_window,"Telephone")
        Telephone.insert(0,dataSet[1])
        Addres = self.newEntry(new_window,"Addres")
        Addres.insert(0,dataSet[2])
        YearStart = self.newEntry(new_window,"Year Start")
        YearStart.insert(0,dataSet[3])
        Button = self.newButton(new_window,"redact",addButton)

    def redactNumClient(self,dataSet):
        def addButton():
            self.connect.reconect()
            id = self.connect.execIO("Select max(id) From numclient")
            id = id[0][0] 
            fio = Fio.get()
            socstatus = SocialStatus.get()
            city = City.get()
            try:
                tel = Telephone.get() 
                adress = Addres.get()
                int(tel)
                socstatus = int(socstatus)
                if len(tel) <= 11 and len(fio)<50 and socstatus>0 and socstatus<=1000:
                    query  =f"""
                    Update numclient Set idcity = '{city}',idaddres='{adress}',fio = '{fio}',
                    telephone = '{tel}', socialstatus = {SocialStatus.get()} Where id = {dataSet[0]} 
                    """
                    self.connect.reconect()
                    self.connect.exec(query)
                    new_window.destroy()
            except:
                messagebox.showwarning("Error","Вы ввели не число в Telephone")
        new_window = self.newWindow("Add Num Client","300x500")
        City = self.newCombobox(new_window,"City","Select city From allcity ")
        City.set(dataSet[1])
        Addres = self.newCombobox(new_window,"Address","Select addres From addresclient")
        Addres.set(dataSet[2])
        Fio = self.newEntry(new_window,"FIO")
        Fio.insert(0,dataSet[3])
        Telephone  = self.newEntry(new_window,"Telephone")
        Telephone.insert(0,dataSet[4])
        SocialStatus = self.newEntry(new_window,"Social status")
        SocialStatus.insert(0,dataSet[5])
        Button = self.newButton(new_window,"redact",addButton)

    def redactNumEmployeer(self,dataSet):
        def addButton():
            self.connect.reconect()
            id = self.connect.execIO("Select max(id) From numemployee")
            id = id[0][0]
            fio = FIO.get()
            if len(fio)<60:
                query = f"Update numemployee Set fio='{fio}' Where id = {dataSet[0]} "
                self.connect.reconect()
                self.connect.exec(query)
                new_window.destroy()
        new_window = self.newWindow("Redact Num Client", "300x200")
        FIO = self.newEntry(new_window,"FIO")
        FIO.insert(0,dataSet[1])
        Button = self.newButton(new_window,"redact",addButton)

    
    def statisticButton(self):
        def addTab(text):
            tabFrame =ttk.Frame(tabs)
            tabs.add(tabFrame,text=text)
            return tabFrame
        def Tabletab(frame,query,title):
            tree = ttk.Treeview(frame,columns = title,show="headings")
            for column in title :
                tree.heading(column,text=column)
            tree.pack(expand=True,fill="both")
            self.connect.reconect()
            result = self.connect.execIO(query)
            for row in result:
                tree.insert("","end",values=row)
        new_window = self.newWindow("Statistic","2000x400")
        tabs = ttk.Notebook(new_window)
        tabs.pack(expand=True,fill="both")
        first = addTab("1 внутренее соединение без условия")
        query = """SELECT filial.idcity, numclient.fio ,numclient.socialstatus
FROM filial
INNER JOIN numclient ON filial.idcity = numclient.idcity"""
        first = Tabletab(first,query,["idcity","FIO","Social Status"])

        second = addTab("2 внутренее соединение без условия")
        query = """Select agreement.amaunt, filial.name, filial.numofemploeers  
from agreement
INNER JOIN filial ON filial.id = agreement.filial"""
        second = Tabletab(second,query,["amaunt","name","numofemployeers"])

        third = addTab("3 внутренее соединение без условия")
        query = """Select agreement.amaunt, agreement.typeofinsuranse, numclient.idcity
from agreement
INNER JOIN numclient ON numclient.id = agreement.client"""
        third = Tabletab(third,query,["amaunt","typeofinsurance","idcity"])

        third = addTab("1 внутреннее с условием")
        query = """Select agreement.amaunt, numclient.socialstatus ,numclient.id ,agreement.client
from agreement
INNER JOIN numclient ON numclient.id = agreement.client
WHERE agreement.amaunt > 25000;"""
        third = Tabletab(third,query,["amaunt","social status","id","client"])

        third = addTab("2 внутреннее с условием")
        query = """Select agreement.amaunt, numclient.socialstatus ,numclient.id ,agreement.client ,numclient.idcity       
from agreement
INNER JOIN numclient ON numclient.id = agreement.client
WHERE numclient.idcity = 'Москва'"""
        third = Tabletab(third,query,["amaunt","social Status","id","client","numclient","idcity"])

        third = addTab("1 c условием на дату")
        query = """Select agreement.amaunt, numclient.socialstatus  
from agreement
INNER JOIN numclient ON numclient.id = agreement.client
WHERE agreement.dateofconclusion > '2015/05/07'"""
        third = Tabletab(third,query,["amaunt","socil Status"])

        third = addTab("2 c условием на дату")
        query = """Select agreement.amaunt, numclient.socialstatus  
from agreement
INNER JOIN numclient ON numclient.id = agreement.client
WHERE agreement.dateofconclusion < '2015/05/07'"""
        third = Tabletab(third,query,["amaunt","socil Status"])

        third = addTab("Левое соединение")
        query = """Select numclient.fio
from agreement
LEFT JOIN numclient ON numclient.id = agreement.client"""
        third = Tabletab(third,query,["FIO"])


        third = addTab("Правое соединение")
        query = """Select numclient.fio
from   agreement
Right JOIN numclient ON numclient.id = agreement.client;"""
        third = Tabletab(third,query,["FIO"])

        third = addTab("Запрос на запросе через левое соединение")
        query = """SELECT n.id, n.fio, n.telephone, 
       COALESCE(a.filial, 0) AS branch, 
       COALESCE(a.typeofinsuranse, 'Not insured') AS insurance_type
FROM numclient n
LEFT JOIN (
    SELECT client, filial, typeofinsuranse
    FROM agreement
    GROUP BY client, filial, typeofinsuranse
) a ON n.id = a.client
WHERE a.client IS NULL;"""
        third = Tabletab(third,query,["id","fio","telephone","branch","insuance type"])

        third = addTab("Итог без условия")
        query = """SELECT COUNT(*) AS total_agreements
FROM agreement;"""
        third = Tabletab(third,query,["total agreement"])

        third = addTab ("Итог с условием")
        query = """SELECT COUNT(*) AS high_value_agreements
FROM agreement
WHERE amaunt > 50000;"""
        third = Tabletab(third,query,["high value agreements"])

        third = addTab("Итог с условием на группы")
        query = """SELECT typeofinsuranse, COUNT(*) AS agreement_count
FROM agreement
GROUP BY typeofinsuranse
HAVING COUNT(*) > 5;"""
        third = Tabletab(third ,query,["typeofinsuranse","agreement count"])

        third = addTab("Итог запрос группы данные")
        query = """SELECT typeofinsuranse, COUNT(*) AS agreement_count
FROM agreement
WHERE amaunt > 10000
GROUP BY typeofinsuranse
HAVING COUNT(*) > 3;"""
        third = Tabletab(third,query,["typeofinsuranse","agreement_count"])

        third = addTab("Запрос на запросе по принципу итогового запроса")
        query = """SELECT COUNT(*) AS clients_with_multiple_agreements
FROM (
    SELECT client, COUNT(*) AS agreement_count
    FROM agreement
    GROUP BY client
    HAVING COUNT(*) > 2
) AS client_agreement_counts;"""
        third = Tabletab(third,query,["client","agreement count"])

        third = addTab("Запрос с подзапросом")
        query = """SELECT fio, telephone
FROM numclient
WHERE id IN (
    SELECT client
    FROM agreement
    WHERE amaunt > 15000
);
"""
        third = Tabletab(third,query,["fio","telephone"])




    def double_click(self,event): # TODO Реализацию Ивента двойное нажатие по полю лицензия
        new_window = tk.Toplevel(self.root)
        new_window.title("Новое окно")
        new_window.geometry("250x200")
        sel = self.MyTables[6].tree.selection()
        sel = self.MyTables[6].tree.item(sel)['values']
        print(type(sel[1]))
        # Добавляем padding, если его не хватает
        missing_padding = len(sel[1]) % 4
        if missing_padding != 0:
                sel[1] += '=' * (4 - missing_padding)
        image_data = base64.b64decode(sel[1])
        image = Image.open(BytesIO(image_data))
        photo = ImageTk.PhotoImage(image)

    def serch(self):
        tables = allTables()
        noteSelect = self.notebook.select()
        if ".!notebook.!frame" == noteSelect:
            tab = 0
        else :
            tab = int(noteSelect[-1]) - 1
            if tab == -1:
                tab = 9
        for item in self.MyTables[tab].tree.get_children():
            self.MyTables[tab].tree.delete(item)

        table = []
        field = tables[tab].getfield()
        for titel in field:
            try:
                query = f"""Select * From {tables[tab].GetTitel()} Where {field[titel]} = '{self.serchEntry.get()}' """
                self.connect.reconect()
                table.append(self.connect.execIO(query))
            except:
                pass
        for item in table:
            if len(item)>0:
                for row in item:
                    self.MyTables[tab].tree.insert("", "end",values=row)
        
    def ressetSearch(self):
        tables = allTables()
        noteSelect = self.notebook.select()
        if ".!notebook.!frame" == noteSelect:
            tab = 0
        else :
            tab = int(noteSelect[-1]) - 1
            if tab == -1:
                tab = 9
        for item in self.MyTables[tab].tree.get_children():
            self.MyTables[tab].tree.delete(item)
            self.filingTables(tables[tab].GetTitel(),tab)

    def GenerateExelFilie(self):
        tables = allTables()
        noteSelect = self.notebook.select()
        if ".!notebook.!frame" == noteSelect:
            tab = 0
        else :
            tab = int(noteSelect[-1]) - 1
            if tab == -1:
                tab = 9
        result_table = self.MyTables[tab].tree
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])

        if not file_path:
            return  

        data = []
        columns = result_table["columns"]  
        for row in result_table.get_children():
            data.append(result_table.item(row, 'values'))

        df = pd.DataFrame(data, columns=columns)
        try:
            df.to_excel(file_path, index=False, engine='openpyxl')
            messagebox.showinfo("Экспорт завершен", "Данные успешно экспортированы в Excel!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при экспорте в Excel: {e}")
        


if __name__ == "__main__":
    window = mainWindow()
    window.exec()
    window.Start()