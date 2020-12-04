from database import setup_db
from logic import checkin_time
from user import add_user, get_all_users, get_user, check_exists
from email_validator import validate_email, EmailNotValidError
from   fastapi import FastAPI, Request, Response, HTTPException
import uvicorn
import json

app = FastAPI()


@app.get('/api/users')
def fetch_all():
    return json.dumps(get_all_users())


@app.get('/api/get')
def get(id:int = 0):
    if check_exists(id):
        return get_user(id)
    else:
        return None

@app.put('/api/add_user')
async def add(request:Request):
    data = await request.json()
    rfid = data['metadata']['id']
    username = data['metadata']['username']
    email = data['metadata']['email']
    try: 
        valid = validate_email(email)
        email = valid.email
    except:
        return HTTPException(status_code=500, detail="Email or id not valid")
    
    recored = add_user(rfid,username,email)
    return recored
maximum = 50
current = 0

@app.get('/api/checkin')
def checkin(id:int = 0):
    global maximum, current
    if check_exists(id) and current < maximum:
        current += 1
        checkin_time(id,'in')
        return [True,current]
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

if __name__ == "__main__":
    setup_db()
    uvicorn.run(app)
    
