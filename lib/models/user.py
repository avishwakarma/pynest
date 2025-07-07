from sqlalchemy import Column, String
from .base_model import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_active = Column(String, default="true")