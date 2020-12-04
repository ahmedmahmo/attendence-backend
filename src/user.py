from   fastapi import HTTPException
from database import connect
from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

def add_user(id:int, username:str, email:str):
    connection = connect()
    cursor = connection.cursor()
    try:
        user = cursor.execute('INSERT INTO users (id, username, email) VALUES (%s, %s, %s)',
                            (id, username, email))
        connection.commit()
        return {'msg' : 'recored created'}
    except (Exception, psycopg2.Error) as error :
        msg = f'Error while fetching user data: {error}'
        return HTTPException(status_code=500, detail=msg)

def get_all_users():
    connection = connect()
    cursor = connection.cursor()
    try:
        get = cursor.execute(f'SELECT * FROM users')
        user_data = cursor.fetchall()
        return user_data
    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching user data: ", error)

def get_user(id:int):
    connection = connect()
    cursor = connection.cursor()
    try:
        get = cursor.execute(f'SELECT * FROM users WHERE id={id}')
        user_data = cursor.fetchone()
        return user_data
    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching user data: ", error)

def check_exists(id:int):
    connection = connect()
    cursor = connection.cursor()
    try:
        cursor.execute(f'SELECT id FROM users WHERE id={id}')
        check = cursor.fetchone() 
        if check == None:
            return False
        else:
            return True
    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching user data: ", error)