from   fastapi import HTTPException
from database import connect
from dotenv import load_dotenv
from datetime import datetime
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
    try:
        cursor.execute(f"SELECT * FROM timestamps WHERE date::DATE BETWEEN DATE '{d_1}' AND DATE '{d_2}';")
        return cursor.fetchall()
    except (Exception, psycopg2.Error) as error :
        msg = f'Error while fetching user data: {error}'
        return HTTPException(status_code=500, detail=msg)

print(get_ondate('2020-12-24','2020-12-25'))