import sqlite3
from sqlite3 import Error

class SQLiteDB(object):
    def __init__(self):
        self.create_table = """
             CREATE TABLE IF NOT EXISTS assigments (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name_assig TEXT NOT NULL,
                 author TEXT NOT NULL,
                 executor TEXT NOT NULL,
                 date_assig DATE,
                 date_completion DATE,
                 dateline DATE,
                 content TEXT NOT NULL
             );  
             """
        self.create_assigment = """
            INSERT INTO
                assigments (name_assig, author, executor, date_assig, date_completion, dateline, content)
            VALUES
                ('Заказ док-ов', 'Сергей', 'Дмитрий', '12.10.2021', '13.10.2012', '14.09.2052', 'Срочно сделать заказ документов, иначе уволю!')
            """

        self.select_all_assigment = "SELECT * from assigments"
        self.search_author = """select * from assigments where author = ?"""
        self.search_executor = """select * from assigments where executor = ?"""
        self.search_date_assigment = """select * from assigments where date_assig = ?"""

    def create_connection(self, path):
        conn = None
        try:
            conn =  sqlite3.connect(path)
            print("Connection to data base " + str(path) + " is successful")
        except Error as e:
            print("Connection to data base " + str(path) + " failed")

        return conn

    def execute_read_query(self, connection, query):
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")

    def search_in_DB(self, request, text):
        try:
            sqlite_connection = sqlite3.connect('db.sqlite')
            cursor = sqlite_connection.cursor()
            sql_request =  request
            cursor.execute(sql_request, (text,))
            sqlite_connection.commit()
            result = cursor.fetchall()
            cursor.close()
            return result

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")

    def update_sqlite_table(self, name_assig, author, executor, date_assig, date_completion, dateline, content, id):
        try:
            sqlite_connection = sqlite3.connect('db.sqlite')
            cursor = sqlite_connection.cursor()
            sql_update_query = """Update assigments set name_assig = ?,
                                                        author = ?,
                                                        executor = ?,
                                                        date_assig = ?,
                                                        date_completion = ?,
                                                        dateline = ?,
                                                        content = ?
                                                        where id = ?"""
            cursor.execute(sql_update_query, (name_assig, author, executor, date_assig, date_completion, dateline, content, id,))
            sqlite_connection.commit()
            cursor.close()
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()

    

    def insert_varible_into_table(self, name_assig, author, executor, date_assig, date_completion, dateline, content):
        try:
            sqlite_connection = sqlite3.connect('db.sqlite')
            cursor = sqlite_connection.cursor()
            flag_connect = True
            sqlite_insert_with_param = """INSERT INTO assigments
                                  (name_assig, author, executor, date_assig, date_completion, dateline, content)
                                  VALUES (?, ?, ?, ?, ?, ?, ?);"""
            data_tuple = (name_assig, author, executor, date_assig, date_completion, dateline, content)
            for i in data_tuple:
                if i == '':
                    print("Одно или несколько полей не заполнены. Невозможно добавить запись")
                    sqlite_connection.close()
                    flag_connect = False
                    break
            if flag_connect == True:
                cursor.execute(sqlite_insert_with_param, data_tuple)
                sqlite_connection.commit()
                print("Переменные Python успешно вставлены в таблицу sqlitedb_developers")
                cursor.close()
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")

    def get_database_table(self, path):
        self.table = self.execute_read_query(self.create_connection(path), self.select_all_assigment)
        return self.table

 
    


