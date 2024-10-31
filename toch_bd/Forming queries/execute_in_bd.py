import psycopg2

class Execute:
    def __init__ (self):
        self.__dbname ='For_lab'
        self.__user = 'postgres'
        self.__password='noinput'
        self.__host='127.0.0.1'
        self.connection = psycopg2.connect(dbname=self.__dbname, user=self.__user, password=self.__password, host=self.__host)
        self.connection.autocommit = True

    def reconect(self):
        self.connection = psycopg2.connect(dbname=self.__dbname, user=self.__user, password=self.__password, host=self.__host)
        self.connection.autocommit = True
    
    def exec (self,command:str): 
        with self.connection.cursor() as cursor:
            cursor.execute(command)
    
    def execTwoArguments  (self,command:str,second):
        with self.connection.cursor() as cursor:
            cursor.execute(command,second)

    def execIO(self,command:str)->str:
        with self.connection.cursor() as cursor:
            cursor.execute(command)
            return cursor.fetchall()