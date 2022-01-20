from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from models.users import  User
from pydantic import BaseModel


router = APIRouter(
    prefix= "/api/v1",
)

router_users = APIRouter(
    prefix="/api/v1/users",
    tags=["users"]
)

router_tasks = APIRouter(
    prefix= "/api/v1/task",
    tags=["tasks"]
)




users=[]

@router.get("/")
def index():
    return {"message":"Hi first time here!"}

#create a new user
@router.post("/signup", status_code=201)
def create_user(user:User):
    new_user = {
        "username": user.username,
        "password": user.password,
        "email":user.email
    }
    users.append(new_user)

    return new_user



@router_users.get("/",summary="List of Users", description="Returns all Users", response_model=List[User])
async def get_users():
    return users


class Settings(BaseModel):
    auth_secret_key:str='6e00f13c55fc9fc63100b3085126e6497a22e542eaac9c8375efb740c1535e5f'


@AuthJWT.load_config
def get_config():
    return Settings()


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


@router.post('/login')
def login(user:UserLogin,Authorize:AuthJWT=Depends()):
    for u in users:
        print(users,"malksmcklsmdvclskv")
        print(u["username"], "dfgshjjhjgfdsgfghjgfdgh")
        if (u["username"]==user.username) and (u["password"]==user.password):
            access_token=Authorize.create_access_token(subject=user.username)
            # refresh_token=Authorize.create_refresh_token(subject=user.username)

            return {"access_token":access_token}

        raise HTTPException(status_code='401',detail="Invalid username or password")