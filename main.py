from fastapi import FastAPI
from routers import users
from database import *


app = FastAPI(title='Users.ly', description='APIs for User and Tasks', version='0.1')


@app.on_event("startup")
async def startup():
    if conn.is_closed():
        conn.connect()




app.include_router(users.router_users)
app.include_router(users.router)


@app.on_event("shutdown")
async def shutdown():
    print("Closing...")
    if not conn.is_closed():
        conn.close()