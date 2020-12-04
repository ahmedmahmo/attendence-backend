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