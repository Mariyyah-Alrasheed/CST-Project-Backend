import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# قراءة رابط قاعدة البيانات من متغير البيئة
DATABASE_URL = os.getenv("DATABASE_URL")

# إنشاء الاتصال
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()