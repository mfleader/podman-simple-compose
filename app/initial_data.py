import asyncio, functools, logging

import databases
import fastapi_users as fastusr


import app.models.models as mdl
from app.main import env
import app.db.base as base


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def async_adapter(wrapped_func):
    @functools.wraps(wrapped_func)
    def run_sync(*args, **kwargs):
        loop = asyncio.new_event_loop()
        task = wrapped_func(*args, **kwargs)
        return loop.run_until_complete(task)
    return run_sync


@async_adapter
async def seed_superuser() -> None:
    """Seed db with a superuser"""
    database = databases.Database(env('DB_URL'))
    await database.connect()
    user_db = fastusr.db.SQLAlchemyUserDatabase(
        user_db_model = mdl.UserDB, 
        database = database, 
        users = base.UserTable.__table__
    )

    su = mdl.UserDB(
            email = env('FIRST_SUPERUSER'),
            hashed_password = fastusr.password.get_password_hash(
                env('FIRST_SUPERUSER_PASSWORD')),
            is_superuser = True
        )
    print(su)
    user = await user_db.get_by_email(su.email)
    if not user:
        await user_db.create(su)

    await database.disconnect()


def main() -> None:
    logger.info("Creating initial data")
    # refactor database startup for reuse
    seed_superuser()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
