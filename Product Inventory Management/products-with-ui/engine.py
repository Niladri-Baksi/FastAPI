from sqlalchemy import create_engine
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
import os

load_dotenv()

username = os.getenv("DB_username")
password = quote_plus(os.getenv("DB_password"))
host = os.getenv("DB_host")
database = os.getenv("DB_database")

db_url = f"mysql+pymysql://{username}:{password}@{host}/{database}"

engine = create_engine(db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #sessionmaker is a factory for creating new Session objects. It is used to configure the behavior of the sessions that will be created. In this case, it is configured to not automatically commit changes to the database (autocommit=False) and to not automatically flush changes to the database (autoflush=False). The bind=engine argument specifies that the sessions created by this sessionmaker will be bound to the specified engine, which is connected to the MySQL database.
