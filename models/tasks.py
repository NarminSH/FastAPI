from peewee import *
import datetime
from database import BaseModel
from .users import User



# class Task(BaseModel):
#     user = ForeignKeyField(User, backref='tasks')
#     title = CharField(max_length=50)
#     created_at = DateTimeField(default=datetime.datetime.now)

