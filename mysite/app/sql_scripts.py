import psycopg2
from decouple import config



def addPerson(name):
    def execute(cursor):
        stmt = f"Insert INTO Person (Name, Status) Values ('{name}', 'Active');"
        cursor.execute(stmt)
    return execute

def executeSQL(commands):
    try:
        connection = psycopg2.connect(user = config("DB_USER"),
                                      password = config("DB_PASSWORD"),
                                      host = config("DB_HOST"),
                                      port = config("DB_PORT"),
                                      database = config("DB_NAME"))
        cursor = connection.cursor()
        for command in commands:
            command(cursor)
        connection.commit()

    except psycopg2.Error as e:
        print(e)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed.")