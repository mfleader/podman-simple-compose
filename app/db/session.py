from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import environs


env = environs.Env()
env.read_env()
engine = create_engine(env('DB_URL'), pool_pre_ping = True)
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)