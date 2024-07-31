from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

# 데이터베이스 엔진 생성
engine = create_engine(DATABASE_URL)

# 기본 클래스를 생성합니다.
Base = declarative_base()

# 세션 생성
Session = sessionmaker(bind=engine)
