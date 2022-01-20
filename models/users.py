from peewee import *
from pydantic import BaseModel


# class User(BaseModel):
#     username = CharField(unique=True, max_length=50, null=False)
#     password = CharField()
#     email = CharField(max_length=40, null=False)
#     created_at = DateTimeField(default=datetime.datetime.now)
#     updated_at = DateTimeField()



# async def create_user(username: str, email: str, password:str):
#     user_object = User(
#         username=username,
#         email=email,
#         password=password
#     )
#     user_object.save()
#     return user_object




class User(BaseModel):
    username  :str
    email     :str
    password  :str

    class Config:
        schema_extra={
            "example":{
                "username":"narminsh",
                "email":"nnkhan@gmail.com",
                "password":"password123"
            }
        }


class UserLogin(BaseModel):
    username:str
    password:str

    class Config:
        schema_extra={
            "example":{
                "username":"nermin",
                "password":"password321"
            }
        }