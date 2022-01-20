
from logging import currentframe
from os import access, stat
from fastapi import FastAPI,Depends,HTTPException,status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from typing import List
from fastapi_jwt_auth import AuthJWT
# from pydantic.networks import url_regex
# from starlette.status import HTTP_401_UNAUTHORIZED
from database import conn


app=FastAPI()

class Settings(BaseModel):
    authjwt_secret_key:str='6e00f13c55fc9fc63100b3085126e6497a22e542eaac9c8375efb740c1535e5f'


@AuthJWT.load_config
def get_config():
    return Settings()

class User(BaseModel):
    username:str
    email:str
    password:str

    class Config:
        schema_extra={
            "example":{
                "username":"narmin",
                "email":"nnkhan@gmail.com",
                "password":"password"
            }
        }

# User.create_table()


class UserLogin(BaseModel):
    username:str
    password:str

    class Config:
        schema_extra={
            "example":{
                "username":"nrmin",
                "password":"password"
            }
        }



users=[]

@app.on_event("startup")
async def startup():
    if conn.is_closed():
        conn.connect()



@app.get("/")
def index():
    return {"message":"Hello"}


#create a user
@app.post('/api/v1/signup',status_code=201)
def create_user(user:User):
    new_user={
        "username":user.username,
        "email":user.email,
        "password":user.password
    }

    users.append(new_user)

    return new_user

#getting all users
@app.get('/api/v1/users',response_model=List[User])
def get_users():
    return users


@app.post('/api/v1/login')
def login(user:UserLogin,Authorize:AuthJWT=Depends()):
    for u in users:
        if (u["username"]==user.username) and (u["password"]==user.password):
            access_token=Authorize.create_access_token(subject=user.username)
            refresh_token = Authorize.create_refresh_token(subject=user.username)

            return {"access_token":access_token, "refresh_token": refresh_token}

        raise HTTPException(status_code='401',detail="Invalid username or password")



@app.post('/api/v1/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}


@app.on_event("shutdown")
async def shutdown():
    print("Closing...")
    if not conn.is_closed():
        conn.close()