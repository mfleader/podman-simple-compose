from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import env


engine = create_engine(env('DB_URL'), pool_pre_ping = True)
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)