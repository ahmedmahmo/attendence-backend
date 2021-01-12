from database import setup_db
from logic import checkin_time,get_ondate
from user import add_user, get_all_users, get_user, check_exists, delete_user
from email_validator import validate_email, EmailNotValidError
from   fastapi import FastAPI, Request, Response, HTTPException
import uvicorn
import json
import os

app = FastAPI()

@app.get('/api/users')
def fetch_all():
    return get_all_users()

@app.get('/api/get')
def get(id:int = 0):
    if check_exists(id):
        return get_user(id)
    else:
        return {"Error_msg": "Id does not exist!"}

@app.put('/api/add_user')
async def add(request:Request):
    data = await request.json()
    rfid = data['id']
    username = data['username']
    email = data['email']
    name = data['name']
    try: 
        valid = validate_email(email)
        email = valid.email
    except:
        return HTTPException(status_code=500, detail="Email or id not valid")
    
    recored = add_user(rfid,username,email,name)
    return recored

maximum = 50
current = 0

@app.get('/api/checkin')
def checkin(id:int = 0):
    global maximum, current
    if check_exists(id) and current < maximum:
        current += 1
        checkin_time(id,'in')
        return [True,current,checkin_time(id,'in')]
    else:
        return False

@app.get('/api/totall')
def totall():
    global maximum, current
    return current

@app.get('/api/checkout')
def checkin(id:int = 0):
    global maximum, current
    if check_exists(id) and current > 0:
        current -= 1
        checkin_time(id,'out')
        return [True,current]
    else:
        return HTTPException(status_code=500,detail='The number of the checkout can not be less than 0')

@app.get('/api/get_ondate')
def get_all_ondate(start:str,end:str):
    return get_ondate(start,end)

@app.get('/api/set_max')
def set_max(max:int):
    global maximum
    maximum = max
    return {"msg": f'Max have been changed to {max}'}

@app.get('/api/get_max')
def get_max():
    global maximum
    return maximum

@app.get('/api/get_current')
def get_max():
    global current
    return current

@app.delete('/api/delete_user')
def delete(id:int):
    return delete_user(id)

@app.get('/')
def test():
    return {"test": {"id": 123}}

if __name__ == "__main__":
    setup_db()
    uvicorn.run(app,host='0.0.0.0',port=8000)
    
