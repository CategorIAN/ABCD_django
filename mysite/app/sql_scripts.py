import psycopg2
from decouple import config
import pandas as pd

def addPerson(name):
    def execute(cursor):
        stmt = f"Insert INTO Person (Name, Status) Values ('{name}', 'Active');"
        cursor.execute(stmt)
    return execute

def request(person, form, timestamp):
    def execute(cursor):
        stmt = (f"Insert INTO form_requests (Person, Form, Timestamp) VALUES "
                        f"{(person, form, timestamp)};".replace("''", "NULL"))
        cursor.execute(stmt)
    return execute

def invite(event, timestamp, person, response, plus_ones, result):
    def execute(cursor):
        stmt = (f"Insert INTO Invitation (Event, Timestamp, Person, Response, Plus_Ones, Result) VALUES "
                f"{(event, timestamp, person, response, plus_ones, result)};").replace("''", "NULL")
        cursor.execute(stmt)
    return execute

def queried_df(cursor, query):
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    data = [[str(x) for x in tuple(y)] for y in cursor.fetchall()]
    return pd.DataFrame(data=data, columns=columns)

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

def readSQL(query):
    try:
        connection = psycopg2.connect(user = config("DB_USER"),
                                      password = config("DB_PASSWORD"),
                                      host = config("DB_HOST"),
                                      port = config("DB_PORT"),
                                      database = config("DB_NAME"))
        cursor = connection.cursor()
        df = queried_df(cursor, query)
        return df

    except psycopg2.Error as e:
        print(e)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed.")