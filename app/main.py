import os, pathlib

import fastapi as fast
import environs
import aiofiles
import starlette as star
import fastapi_users as fastusr
import databases
from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask
from flask_autoindex import AutoIndex

import app.db.base as base
import app.models.models as mdl


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = '/'.join((ROOT_DIR, 'results'))
print(RESULTS_DIR)
env = environs.Env()
env.read_env(recurse=False)
DATABASE_URL = env('DB_URL')
SECRET = env('SECRET')
HOST = env('DATA_SERVER_PUBLIC_HOST')
PORT = env('DATA_SERVER_PORT') 
VALID_EXTENSIONS = (
    '.png', '.jpeg', '.jpg',
    '.tar.gz', '.tar.xz', '.tar.bz2'
)


app = fast.FastAPI()
database = databases.Database(DATABASE_URL)
jwt_authentication = fastusr.authentication.JWTAuthentication(
    secret=SECRET, lifetime_seconds=3600,
    tokenUrl='/auth/jwt/login')
cookie_authentication = fastusr.authentication.CookieAuthentication(
    secret=SECRET, lifetime_seconds=3600)
api_users = fastusr.FastAPIUsers(
    db = fastusr.db.SQLAlchemyUserDatabase(
        user_db_model = mdl.UserDB, 
        database = database, 
        users = base.UserTable.__table__),
    auth_backends = [
        jwt_authentication,
        cookie_authentication
    ],
    user_model = mdl.User,
    user_create_model = mdl.UserCreate,
    user_update_model = mdl.UserUpdate,
    user_db_model = mdl.UserDB,
)


# Flask AutoIndex module for exploring directories
flask_app = Flask(__name__)
AutoIndex(flask_app, browse_root = RESULTS_DIR)
app.mount('/results', WSGIMiddleware(flask_app))


@app.get('/')
async def root(): 
    return star.responses.RedirectResponse(url = '/docs')


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


def on_after_register(user: mdl.UserDB, request: fast.Request):
    print(f"User {user.id} has registered.")


app.include_router(
    api_users.get_auth_router(jwt_authentication),
    prefix = '/auth/jwt',
    tags = ['auth']
)
app.include_router(
    api_users.get_register_router(on_after_register),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    api_users.get_users_router(), 
    prefix = '/users', 
    tags=['users']
)
