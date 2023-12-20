from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL ="mssql+pyodbc://(localdb)\\MSSQLLocalDB/ChatDb?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"
  # Replace with your database connection string

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal will be used to create individual database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
