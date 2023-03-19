import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DATETIME, String
from datetime import datetime

db_engine = sqlalchemy.create_engine(
    'sqlite:////vol/haikudb.sqlite3',
    echo=True
)

Base = declarative_base()


class Haiku(Base):
    __tablename__ = "haiku"
    id = Column('id', Integer(), primary_key=True)
    created_at = Column(
        'created', DATETIME(), nullable=False, default=datetime.now
    )
    # 自由律俳句もサポートするため，100文字まで許容
    content = Column('content', String(length=100), nullable=False)
