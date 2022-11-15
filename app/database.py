from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
#  ----we are using sqlalchemy to connect to the database ...the below are the direct way to connect using the pcycopg driver   

# while True: # created a loop in order to try every 2 seconds to connect, if it manages breaks out of the loop
    
#     try:
#         conn = psycopg2.connect(host='localhost', database='GreekReads',
#                                 user='postgres', password='kalakrasa', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection successful")
#         break
#     except Exception as error:
#         print("Connection to DB failed")
#         print("Error", error)
#         time.sleep(2)