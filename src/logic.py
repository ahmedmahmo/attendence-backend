from   fastapi import HTTPException
from database import connect
from dotenv import load_dotenv
from datetime import datetime
import json
import psycopg2
import os

load_dotenv()

def checkin_time(id:int,state:str):
    connection = connect()
    cursor = connection.cursor()
    try:
        dt = datetime.now()
        user = cursor.execute('INSERT INTO timestamps (id, date,state) VALUES (%s, %s, %s)',
                            (id, dt, state))
        connection.commit()
        return {'msg' : f'{id} checked{state} in at {dt}'}
    except (Exception, psycopg2.Error) as error :
        msg = f'Error while fetching user data: {error}'
        return HTTPException(status_code=500, detail=msg)

def get_ondate(d_1:str,d_2:str):
    connection = connect()
    cursor = connection.cursor()
    user_data = []
    try:
        cursor.execute(f"SELECT * FROM timestamps WHERE date::DATE BETWEEN DATE '{d_1}' AND DATE '{d_2}';")
        all = cursor.fetchall()
        for user in all:
            id = user[0]
            date = user[1]
            state = user[2]
            cursor.execute(f'SELECT username FROM users WHERE id={id}')
            username = cursor.fetchone()
            cursor.execute(f'SELECT name FROM users WHERE id={id}')
            name = cursor.fetchone()
            text = {"id": id,
                    "name": name,
                    "username": username,
                    "state": state,
                    "datetime": date}
            user_data.append(text)
        return user_data
        
    except (Exception, psycopg2.Error) as error :
        msg = f'Error while fetching user data: {error}'
        return HTTPException(status_code=500, detail=msg)

print(get_ondate('2021-01-08','2021-01-08'))