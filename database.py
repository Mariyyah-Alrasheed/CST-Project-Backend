import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# تحميل متغيرات البيئة من ملف .env
load_dotenv()

# قراءة الرابط
DATABASE_URL = os.getenv("DATABASE_URL")

# تحقق من وجود الرابط
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL not found. تأكدي إنه معرف في .env")

# إنشاء الاتصال
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
