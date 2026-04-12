import os
import time
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:postgres@db:5432/dbname")
DB_RETRY_COUNT = int(os.getenv("DB_RETRY_COUNT", "10"))
DB_RETRY_DELAY = float(os.getenv("DB_RETRY_DELAY", "2"))

# retry connection
for i in range(DB_RETRY_COUNT):
    try:
        engine = create_engine(DATABASE_URL, echo=True)
        conn = engine.connect()
        conn.close()
        break
    except Exception:
        print(f"DB not ready, retrying ... ({i + 1}/{DB_RETRY_COUNT})")
        time.sleep(DB_RETRY_DELAY)

# 👇 TO MUSI BYĆ POZA PĘTLĄ
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 👇 I TO TEŻ POZA PĘTLĄ
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()