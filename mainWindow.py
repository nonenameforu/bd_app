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
import io


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
    
    def addCity(self): # TODO добавить проверку на пустоту
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
                self.connect.exec(f"Insert Into allcity Values('{Date.get_date()}')")
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


    def redactButton(self): # TODO Реализацию кнопки Редактировать
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
        print(dataSet[8])
        TyepOfInsurance.set(dataSet[8])

        Button = self.newButton(new_window,"redact",addButton)
    
    def statisticButton(self): # TODO Реализацию кнопки статистика
        pass

    def double_click(self,event): # TODO Реализацию Ивента двойное нажатие по полю лицензия
        new_window = tk.Toplevel(self.root)
        new_window.title("Новое окно")
        new_window.geometry("250x200")
        
        # Добавление виджетов в новое окно
        label = tk.Label(new_window, text="Это новое окно")
        label.pack()


if __name__ == "__main__":
    window = mainWindow()
    window.exec()
    window.Start()