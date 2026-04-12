from sqlalchemy import Column, Integer, String
from src.database import Base

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    password = Column(String(255), nullable=False)