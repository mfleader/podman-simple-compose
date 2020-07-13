import os

import uvicorn
from fastapi import FastAPI
import environs
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi_sqlalchemy import db
from models import User as ModelUser
from schema import User as SchemaUser



ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

env = environs.Env()
env.read_env()

app = FastAPI()

app.add_middleware(DBSessionMiddleware, 
    db_url=env('DB_URI')
)


@app.post("/user/", response_model=SchemaUser)
async def create_user(user: SchemaUser):
    db_user = ModelUser(
        first_name=user.first_name, last_name=user.last_name, age=user.age
    )
    db.session.add(db_user)
    db.session.commit()
    return db_user



