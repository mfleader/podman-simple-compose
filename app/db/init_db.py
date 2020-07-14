import asyncio, functools

from fastapi_users.password import get_password_hash

import app.models.models as mdl
from app.main import (api_users, env)

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def async_adapter(wrapped_func):
    @functools.wraps(wrapped_func)
    def run_sync(*args, **kwargs):
        loop = asyncio.new_event_loop()
        task = wrapped_func(*args, **kwargs)
        return loop.run_until_complete(task)
    return run_sync


@async_adapter
async def init_db() -> None:
    """Seed db with a superuser"""
    su = mdl.UserDB(
            email = env('FIRST_SUPERUSER'),
            hashed_password = get_password_hash(env('FIRST_SUPERUSER_PASSWORD'))
        )
    print(su)
    user = await api_users.db.get_by_email(su.email)
    
    print(user)



if __name__ == '__main__':
    init_db()


