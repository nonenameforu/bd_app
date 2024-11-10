import psycopg2
import execute_in_bd
import random
from PIL import Image, ImageDraw
from io import BytesIO


# Список имен
name = ["Алексей", "Дмитрий", "Иван", "Николай", "Егор", "Андрей", "Михаил", "Сергей", "Александр", "Кирилл"]

# Список отчеств
patronymic = ["Алексеевич", "Дмитриевич", "Иванович", "Николаевич", "Егорович", "Андреевич", "Михайлович", "Сергеевич", "Александрович", "Кириллович"]

# Список фамилий
surname = ["Петров", "Иванов", "Сидоров", "Федоров", "Смирнов", "Кузнецов", "Попов", "Соколов", "Орлов", "Морозов"]

# Создаем список из 300 названий улиц, типичных для России, используя Python
streets_list = [
    "Ленина", "Советская", "Мира", "Гагарина", "Пушкина", "Школьная", "Комсомольская", 
    "Садовая", "Октябрьская", "Молодежная", "Зеленая", "Набережная", "Первомайская", 
    "Железнодорожная", "Пролетарская", "Кирова", "Центральная", "Рабочая", "Лесная", 
    "Пионерская", "Новая", "Красная", "Юбилейная", "Заречная", "Парковая", "Спортивная", 
    "Строителей", "Трудовая", "Чапаева", "Заводская", "Колхозная", "Огородная", "Весенняя", 
    "Восточная", "Западная", "Северная", "Южная", "Луговая", "Космонавтов", "Вокзальная", 
    "Береговая", "Энергетиков", "Северная", "Аэропортовская", "Лермонтова", "Калинина", 
    "Речная", "Почтовая", "Индустриальная", "Больничная", "Клубная", "Урожайная", "Бережная",
    "Радужная", "Краснодарская", "Лазурная", "Морская", "Дружбы", "Подгорная", "Заводская",
    "Дружбы Народов", "Малая", "Сиреневая", "Ясеневая", "Бульвар", "Приморская", "Березовая",
    "Лунная", "Песчаная", "Кедровая", "Цветочная", "Еловая", "Гранитная", "Крайняя", 
    "Малая Садовая", "Большая Садовая", "Солнечная", "Уютная", "Озерная", "Портовая",
    "Профсоюзная", "Производственная", "Артема", "Тихая", "Мельничная", "Благодатная", 
    "Машиностроителей", "Хуторская", "Тракторная", "Промышленная", "Писателя Горького", 
    "Горная", "Транспортная", "Ботаническая", "Тенистая", "Свободы", "Городская", 
    "Чкалова", "Комарова", "Чистопрудная", "Крымская", "Героев", "Сосновая", "Малая Октябрьская",
    "Кавказская", "Майская", "Смоленская", "Тверская", "Тургенева", "Белорусская", "Хорошевская", 
    "Волжская", "Авангардная", "Привокзальная", "Каменная", "Печерская", "Покровская", 
    "Свердлова", "Челюскинцев", "Интернациональная", "Кузнечная", "Кооперативная", "Степная", 
    "Полевая", "Хлебная", "Озерковая", "Павловская", "Куйбышева", "Саянская", "Песчаная", 
    "Авиационная", "Каштановая", "Нагорная", "Профессора", "Студенческая", "Технологическая",
    "Угольная", "Тепличная", "Широкая", "Славянская", "Хвойная", "Песочная", "Глинистая", 
    "Подгорная", "Забайкальская", "Глазкова", "Прибрежная", "Володарского", "Прудная", 
    "Арсеньева", "Розы Люксембург", "Софийская", "Новосельская", "Синяя", "Луначарского",
    "Фрунзе", "Космическая", "Березовая", "Суворова", "Боровая", "Зеленоградская", 
    "Театральная", "Тропическая", "Горького", "Классическая", "Невская", "Каширская", 
    "Стахановская", "Фабричная", "Карьерная", "Портовая", "Малая Набережная", "Академическая", 
    "Сокольническая", "Студенческая", "Болотная", "Спартаковская", "Новолучанская", "Семеновская", 
    "Дмитриевская", "Тургенева", "Уралмашевская", "Малиновая", "Ильинская", "Пионерская", 
    "Праздничная", "Профсоюзная", "Академика Сахарова", "Железнодорожная", "Клименко", 
    "Бердская", "Курчатова", "Парковая", "Морозова", "Каменная", "Невская", "Космонавтов", 
    "Пушкинская", "Космодемьянской", "Караваева", "Тихонравова", "Березка", "Победы", 
    "Бородинская", "Гоголя", "Юрия Гагарина", "Днепровская", "Казахская", "Капитальная", 
    "Ландышевая", "Сосенская", "Соломенская", "Можайская", "Боровская", "Сахалинская", 
    "Тверская", "Кавказская", "Сибирская", "Минская", "Кавказская", "Ростовская", "Старицкая", 
    "Речников", "Академика Павлова", "Рощинская", "Патриотическая", "Тверская", "Шоссейная", 
    "Арсенальная", "Семейная", "Курортная", "Новосельская", "Ново-Садовая", "Малая Невская", 
    "Невская", "Римская", "Озерковая", "Елизаветинская", "Родниковая", "Нижняя", "Новая Рига", 
    "Медовая", "Кипарисовая", "Литературная", "Кожевенная", "Патриотов", "Сумская", "Барнаульская", 
    "Озерковая", "Ключевая", "Вишневая", "Артиллерийская", "Архангельская", "Тракторная", 
    "Ломоносова", "Новосельская", "Лебединая", "Парковая", "Цветочная", "Прибрежная", "Ильинская", 
    "Комарова", "Верхняя", "Огородная", "Ландышевая", "Сиреневая", "Сосенская", "Царская", 
    "Хвойная", "Тенистая", "Глиняная", "Спокойная", "Площадь Победы", "Верхневолжская", 
    "Славянская", "Ветеранов", "Грибоедова", "Невская", "Кедровая", "Федорова", "Крепостная"
]

# Список имен
name = ["Георгий", "Антон", "Владислав", "Максим", "Павел", "Олег", "Степан", "Константин", "Виктор", "Арсений", "Денис", "Роман", "Тимофей"]

# Список отчеств
patronymic = ["Георгиевич", "Антонович", "Владиславович", "Максимович", "Павлович", "Олегович", "Степанович", "Константинович", "Викторович", "Арсеньевич", "Денисович", "Романович", "Тимофеевич"]

# Список фамилий
surname = ["Зайцев", "Волков", "Богданов", "Воробьев", "Гусев", "Медведев", "Титов", "Крылов", "Макаров", "Жуков", "Сафонов", "Родионов", "Ермаков"]


def filingFio(name:list ,patronymic:list ,surname:list):
    fio=[]
    for i in range(len(name)):
        for j in range(len(patronymic)):
            for z in range(len(surname)):
                fio.append(name[i]+" "+patronymic[j]+" "+surname[z])
    return fio
    for i in range(len(fio)):
        table = "numemployee"
        connect.exec("INSERT INTO "+table+" VALUES ("+str(i+1)+",'"+fio[i]+"')")

def filingAddress(street:list,quantity:int):
    address=[]
    prefix=["Улица","Бульвар","Проспект"]
    for i in range(quantity):
        house = random.randint(1,50)
        apartment = random.randint(0,120)
        iStreet = random.randint(0,len(street)-1)
        iPrefix = random.randint(0,len(prefix)-1)
        if apartment != 0 :
            address.append(prefix[iPrefix]+" "+street[iStreet]+" Дом "+str(house)+" Квартира "+str(apartment))
        else:
            address.append(prefix[iPrefix]+" "+street[iStreet]+" Дом "+str(house))
    
    return address

    # adress = filingAddress(streets_list,62)
    # connect = execute_in_bd.Execute()
    # for i in range(len(adress)):
    #     table = "addresclient"
    #     connect.exec("INSERT INTO "+table+" VALUES ('"+adress[i]+"')")
    
def filingNumClient():
    connect = execute_in_bd.Execute()

    city = connect.execIO(""" SELECT * FROM allcity""")
    addres = connect.execIO(""" SELECT * FROM addresclient""")
    fio = filingFio(name,patronymic,surname)
    for i in range(len(addres)):
        number = 79_000_000_000+random.randint(100_000_000,999_999_999)
        socialStatus = random.randint(500,1000)
        request = "INSERT INTO numclient VALUES ("+str(i+1)+",(SELECT city FROM allcity WHERE city = '"+city[random.randint(0,99)][0]+"'),(SELECT addres FROM addresclient WHERE addres = '"+addres[i][0]+"'),'"+fio[i]+"',"+str(number)+","+str(socialStatus)+");"
        print(request)
        connect = execute_in_bd.Execute()
        connect.exec(request)
    IO = connect.execIO(""" SELECT * FROM numclient""")
    print(IO)
    
def filingFilial():
    connect = execute_in_bd.Execute()
    city = connect.execIO(""" SELECT * FROM allcity""")
    adress = filingAddress(streets_list,100)
    for i in range (len(adress)):
        number = 79_000_000_000+random.randint(100_000_000,999_999_999)
        numofemploers = random.randint(4,6)
        year = random.randint(1992,2024)
        request = "INSERT INTO filial VALUES ((SELECT city FROM allcity WHERE city = '"+city[random.randint(0,99)][0]+"'),'Филиал номер "+str(i+1)+"','"+adress[i]+"','"+str(number)+"',"+str(year)+","+str(numofemploers)+","+str(i)+")"
        print(request)
        connect.reconect()
        connect.exec(request)

def filingInsuranceCompany():
    connect = execute_in_bd.Execute()
    types_of_ownership = [
        "Частная собственность",
        "Государственная собственность",
        "Смешанная собственность",
        "Иностранная собственность"
    ]
    for i in range(20):
        request = "INSERT INTO insurancecompany VALUES ("+str(i)+",'Строховая компания "+str(i)+"','"+types_of_ownership[random.randint(0,3)]+"')"
        connect.reconect()
        connect.exec(request)

def filingContractDate():
    # connect = execute_in_bd.Execute()
    #for i in range (2000):
        day = random.randint(1,28)
        month = random.randint(1,12)
        year = random.randint(1993,2024)
        # request = "INSERT INTO contractdate VALUES ('"+str(day)+"."+str(month)+"."+str(year)+"')"
        # connect.reconect()
        # connect.exec(request)
        return str(day)+"."+str(month)+"."+str(year)

def filingLicense():
    connect = execute_in_bd.Execute()
    for i in range(5):
        number = random.randint(100000000,999999999)

        width, height = 200, 200
        image = Image.new("RGB", (width, height), "white")
        # Создаем объект для рисования
        draw = ImageDraw.Draw(image)
        # Рисуем прямоугольник (координаты начала и конца, цвет)
        draw.rectangle([(50, 50), (150, 150)], fill="blue", outline="black")
        # Конвертируем изображение в бинарный формат для передачи
        binary_stream = BytesIO()
        image.save(binary_stream, format="PNG")  # Сохраняем в поток в формате PNG
        binary_data = binary_stream.getvalue()   # Получаем бинарные данные

        date = filingContractDate()

        query = "INSERT INTO license VALUES (%s, %s, %s, %s)"
        values = (i, binary_data, date,number)
        connect.reconect()
        connect.exec(query,values)

def filingMainOffice():
    connect = execute_in_bd.Execute()
    query = "INSERT INTO mainoffice VALUES ((SELECT city FROM allcity WHERE city ='Москва'),'79596665533','Улица Главная дом 5',1992,(SELECT license FROM licnse WHERE id = 0),0)"
    connect.reconect()
    connect.exec(query)

#try:

connect = execute_in_bd.Execute()
date = connect.execIO("SELECT * FROM contractdate;")


# Генерируем запрос для текущего значения i и произвольного типа страхования
types_of_insurance = [
    "Медицинское страхование",
    "Автомобильное страхование",
    "Страхование жизни",
    "Имущественное страхование",
    "Страхование от несчастных случаев",
    "Пенсионное страхование",
    "Страхование путешествий",
    "Страхование бизнеса",
    "Страхование ответственности",
    "Страхование на случай потери работы",
    "Ипотечное страхование",
    "Страхование домашних животных",
    "Страхование от стихийных бедствий"
]

for i in range (len(date)):
    type_of_insurance = random.choice(types_of_insurance)
    summa = random.randint(15000,150000)

    query = f"""
        INSERT INTO agreement VALUES (
            {i}, {summa}, 'договор {i}',
            (SELECT id FROM filial WHERE id = {random.randint(0, 99)}),
            (SELECT id FROM numclient WHERE id = {i+1}),
            (SELECT id FROM numemployee WHERE id = {random.randint(1, 1000)}),
            (SELECT id FROM insurancecompany WHERE id = {random.randint(0, 19)}),
            (SELECT datecontract FROM contractdate WHERE datecontract = '{date[i][0]}'),
            '{type_of_insurance}',
            (SELECT id FROM mainoffice WHERE id = 0)
        );
    """

    print(query)

    connect.reconect()
    connect.exec(query)


# except:
#     print('Can`t establish connection to database')