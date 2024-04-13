import psycopg2
from psycopg2 import IntegrityError
from settings.config import Setting


class MyPostgreSQL:
    def __init__(self, database, user, password, host, port=5432):
        self.connection = None
        try:
            self.connection = psycopg2.connect(
                                database=database,
                                user=user,
                                password=password,
                                host=host,
                                port=port)
            print("Database connected")
        except:
            print("Database not connected")
            raise Exception("Database not connected")
            
        if self.connection is not None:
            self.connection.autocommit = True
        #     cursor = self.connection.cursor()
        #     cursor.execute("SELECT datname FROM pg_database")
        #     list_database = cursor.fetchall()
        #     print("list_database: ", list_database)

    def close(self):
        self.connection.close()
        print('Close connection')

    def check_exists(self, table, condition):
        query = f"SELECT 1 FROM {table} WHERE {condition} LIMIT 1;"
        cursor = self.connection.cursor()
        cursor.execute(query)
        row = cursor.fetchone()
        if not row:
            cursor.close()
            return False
        else:
            cursor.close()
            return True
        
    def insert(self, table=None,  values=None, column = None):
        try:
            if column != None:
                query = f'INSERT INTO {table} ('
                for item in column:
                    query += "\""+item+"\","
                query = query[:len(query)-1] + ')'
                query = f'{query} VALUES {values}'
            else:
                query = f'INSERT INTO {table} VALUES {values};'
            # print(query)
            cursor = self.connection.cursor()
            cursor.execute(query)   
            self.connection.commit()
            cursor.close()
            return True
        except IntegrityError:
            return False

    def update(self, table,  set, condition):
        query = f"UPDATE {table} SET {set} WHERE {condition};"
        # print(query)
        cursor = self.connection.cursor()
        cursor.execute(query)   
        self.connection.commit()
        cursor.close()
        
Database = MyPostgreSQL(database=Setting.POSTGRES_DB, user=Setting.POSTGRES_USER, 
                        password=Setting.POSTGRES_PASSWORD, host=Setting.POSTGRES_HOST, 
                        port=Setting.POSTGRES_PORT)

Database2 = MyPostgreSQL(database=Setting.POSTGRES_DB2, user=Setting.POSTGRES_USER2, 
                        password=Setting.POSTGRES_PASSWORD2, host=Setting.POSTGRES_HOST2, 
                        port=Setting.POSTGRES_PORT2)


